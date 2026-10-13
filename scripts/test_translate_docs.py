"""Focused checks for the documentation translation integration (no API calls)."""

import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import json
import asyncio
import os


MODULE_PATH = Path(__file__).with_name("translate_docs.py")
docs = None
if MODULE_PATH.exists():
    spec = importlib.util.spec_from_file_location("translate_docs", MODULE_PATH)
    docs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(docs)


class TranslationSafetyTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(docs, "The translation integration is not implemented yet")
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.output = self.root / "translations/en"
        self.output.mkdir(parents=True)

    def test_chinese_navigation_is_idempotent_and_preserves_the_body(self):
        original = '<div align="center">\n\n![Banner](image.png)\n\n</div>\n\nOriginal body.\n'
        result = docs.apply_language_switch(
            original, "zh", self.root / "README.md", self.output / "README.md"
        )
        self.assertIn("**简体中文** · [English](translations/en/README.md)", result)
        self.assertEqual(result.count(docs.NAV_START), 1)
        self.assertTrue(result.endswith("Original body.\n"))
        self.assertEqual(
            docs.apply_language_switch(result, "zh", self.root / "README.md", self.output / "README.md"),
            result,
        )

    def test_english_navigation_returns_to_the_chinese_readme(self):
        result = docs.apply_language_switch(
            "# Guide\n\nEnglish body.\n", "en", self.root / "README.md", self.output / "README.md"
        )
        self.assertIn("[简体中文](../../README.md) · **English**", result)

    def test_untranslated_links_fall_back_without_touching_code_or_existing_translations(self):
        (self.root / "FAQ.md").write_text("# FAQ\n")
        (self.root / "Other Guide.md").write_text("# Other guide\n")
        (self.output / "Chapter.md").write_text("# Chapter\n")
        text = (
            '[Help](FAQ.md#details) [English](Chapter.md)\n'
            '<a href="FAQ.md">Help</a>\n'
            '[reference]: <Other Guide.md> "Guide"\n'
            '`[literal](FAQ.md)`\n'
            '```md\n[example](FAQ.md)\n```\n'
        )
        result = docs.repair_local_links(text, self.output / "README.md", self.root)
        self.assertIn("[Help](../../FAQ.md#details)", result)
        self.assertIn("[English](Chapter.md)", result)
        self.assertIn('<a href="../../FAQ.md">', result)
        self.assertIn('<../../Other%20Guide.md>', result)
        self.assertIn('`[literal](FAQ.md)`', result)
        self.assertIn('```md\n[example](FAQ.md)\n```', result)
        self.assertEqual(docs.repair_local_links(result, self.output / "README.md", self.root), result)

    def test_changed_executable_code_is_rejected(self):
        source = self.root / "README.md"
        translated = self.output / "README.md"
        source.write_text("# 原文\n\n```python\nprint('hello')\n```\n")
        translated.write_text("# Translation\n\n```python\nprint('changed')\n```\n")
        with self.assertRaisesRegex(ValueError, "code"):
            docs.validate_document(source, translated, self.root)

    def test_missing_local_link_is_rejected(self):
        source = self.root / "README.md"
        translated = self.output / "README.md"
        source.write_text("# 原文\n\nText.\n")
        translated.write_text("# Translation\n\n[Broken](missing.md)\n")
        with self.assertRaisesRegex(ValueError, "link"):
            docs.validate_document(source, translated, self.root)

    def test_failed_validation_does_not_overwrite_existing_output(self):
        staged = self.root / "staging"
        (staged / "translations/en").mkdir(parents=True)
        (staged / "README.md").write_text("# 原文\n\n```sh\necho safe\n```\n")
        (staged / "translations/en/README.md").write_text("# English\n\n```sh\nrm danger\n```\n")
        existing = self.output / "README.md"
        existing.write_text("Existing accepted translation.\n")
        with self.assertRaises(ValueError):
            docs.publish_translations(staged, self.root, ["README.md"])
        self.assertEqual(existing.read_text(), "Existing accepted translation.\n")

    def test_concurrent_source_edit_is_detected_and_preserved(self):
        path = self.root / "README.md"
        path.write_text("Original.\n")
        snapshot = {"README.md": hashlib.sha256(path.read_bytes()).hexdigest()}
        path.write_text("A user's newer edit.\n")
        with self.assertRaisesRegex(RuntimeError, "changed"):
            docs.verify_sources_unchanged(self.root, snapshot)
        self.assertEqual(path.read_text(), "A user's newer edit.\n")

    def test_gateway_configuration_sends_openai_request_to_the_configured_url(self):
        import httpx
        from openai import AsyncOpenAI
        from openai.resources.chat.completions import AsyncCompletions
        requests = []

        def handle(request):
            requests.append(request)
            return httpx.Response(200, json={
                "id": "test", "object": "chat.completion", "created": 0,
                "model": "example-model", "choices": [{"index": 0,
                "message": {"role": "assistant", "content": "English"}, "finish_reason": "stop"}]})

        async def call():
            async with AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"],
                                   base_url=os.environ["OPENAI_BASE_URL"],
                                   http_client=httpx.AsyncClient(transport=httpx.MockTransport(handle))) as client:
                result = await client.chat.completions.create(
                    model=os.environ["OPENAI_CHAT_MODEL_ID"],
                    messages=[{"role": "user", "content": "Translate"}])
                self.assertEqual(result.choices[0].message.content, "English")

        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test-gateway-key",
                                    "DEEPSEEK_BASE_URL": "https://gateway.example.invalid/",
                                    "DEEPSEEK_MODEL": "example-model"}, clear=True), \
             patch.object(AsyncCompletions, "create", AsyncCompletions.create):
            docs.configure_deepseek(self.root)
            asyncio.run(call())
        self.assertEqual(str(requests[0].url), "https://gateway.example.invalid/v1/chat/completions")
        self.assertEqual(requests[0].headers["Authorization"], "Bearer test-gateway-key")
        payload = json.loads(requests[0].content)
        self.assertEqual(payload["model"], "example-model")
        self.assertEqual(payload["thinking"], {"type": "disabled"})

    def test_official_api_defaults_remain_available(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(docs.translation_api_settings(),
                             ("https://api.deepseek.com/v1", "deepseek-flash"))

    def test_model_or_url_changes_invalidate_translation_cache(self):
        with patch.dict(os.environ, {"DEEPSEEK_BASE_URL": "https://gateway.example.invalid/v1",
                                    "DEEPSEEK_MODEL": "example-model"}, clear=True):
            original = docs.settings_digest()
            os.environ["DEEPSEEK_MODEL"] = "deepseek-flash"
            changed_model = docs.settings_digest()
            self.assertNotEqual(original, changed_model)
            os.environ["DEEPSEEK_BASE_URL"] = "https://api.deepseek.com/v1"
            self.assertNotEqual(changed_model, docs.settings_digest())

    def test_errors_do_not_reveal_private_connection_settings(self):
        private_url = "https://gateway.example.invalid/v1"
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test-private-key",
                                    "DEEPSEEK_BASE_URL": private_url,
                                    "DEEPSEEK_MODEL": "example-private-model"}, clear=True):
            result = docs.redact_error(
                "Request to " + private_url + "/chat/completions at gateway.example.invalid "
                "failed for example-private-model using test-private-key")
        self.assertNotIn(private_url, result)
        self.assertNotIn("gateway.example.invalid", result)
        self.assertNotIn("example-private-model", result)
        self.assertNotIn("test-private-key", result)

    def test_discovery_covers_tracked_nested_docs_but_not_generated_or_local_files(self):
        names = ["README.md", "项目/指南.MD", "_sidebar.md", "_sidebar.en.md",
                 "translations/en/README.md", "scripts/translation-glossary.md"]
        for name in names + ["untracked.md"]:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("# 文档\n")
        with patch.object(docs.subprocess, "check_output", return_value="\0".join(names).encode()):
            self.assertEqual(docs.discover_documents(self.root),
                             ("README.md", "_sidebar.md", "项目/指南.MD"))

    def test_nested_workspace_and_resource_directories_are_preserved(self):
        source = self.root / "项目/指南.md"
        source.parent.mkdir()
        (source.parent / "code").mkdir()
        source.write_text("# 指南\n\n[Code](code/)\n")
        staged = self.root / "staging"
        staged.mkdir()
        snapshots = docs.prepare_workspace(self.root, staged, ["项目/指南.md"])
        self.assertEqual((staged / "项目/指南.md").read_bytes(), source.read_bytes())
        self.assertTrue((staged / "项目/code").is_dir())
        self.assertIn("项目/指南.md", snapshots)

    def test_new_english_docs_replace_chinese_fallback_links_and_share_assets(self):
        (self.root / "FAQ.md").write_text("# FAQ\n")
        (self.root / "image.png").write_bytes(b"image")
        text = "[FAQ](../../FAQ.md) ![Image](../../image.png)\n"
        result = docs.repair_local_links(text, self.output / "README.md", self.root,
                                        translated_files={"README.md", "FAQ.md"})
        self.assertIn("[FAQ](FAQ.md)", result)
        self.assertIn("![Image](../../image.png)", result)

    def test_content_translation_links_use_the_source_location(self):
        text = '[FAQ](../FAQ.md) [Code](code/demo.py) ![Image](/image.png)\n'
        result = docs.repair_local_links(text, self.output / "项目/指南.md", self.root,
                                        source_path=self.root / "项目/指南.md",
                                        translated_files={"项目/指南.md", "FAQ.md"})
        self.assertIn("[FAQ](../FAQ.md)", result)
        self.assertIn("[Code](../../../项目/code/demo.py)".replace("项目", "%E9%A1%B9%E7%9B%AE"), result)
        self.assertIn("![Image](../../../image.png)", result)

    def test_backticks_inside_a_fence_do_not_hide_later_image_links(self):
        text = 'An unmatched ` before a fence.\n\n````text\n`unpaired\n````\n\n![Image](images/example.png)\n\n````text\nend\n````\n'
        result = docs.repair_local_links(text, self.output / "README.md", self.root,
                                        source_path=self.root / "README.md",
                                        translated_files={"README.md"})
        self.assertIn("![Image](../../images/example.png)", result)
        self.assertIn('````text\n`unpaired\n````', result)

    def test_existing_broken_source_link_is_preserved_but_new_broken_link_is_rejected(self):
        source = self.root / "README.md"
        target = self.output / "README.md"
        source.write_text("# 原文\n\n[Old](missing.md)\n")
        target.write_text("# English\n\n[Old](../../missing.md)\n")
        docs.validate_document(source, target, self.root)
        target.write_text("# English\n\n[New](../../different.md)\n")
        with self.assertRaisesRegex(ValueError, "link"):
            docs.validate_document(source, target, self.root)

    def test_generated_site_sidebar_uses_english_routes(self):
        text = "- [Home](README.md)\n- [Chapter](项目/指南.md)\n"
        result = docs.site_sidebar(text, self.root)
        self.assertIn("[Home](/translations/en/)", result)
        self.assertIn("[Chapter](/translations/en/", result)
        self.assertNotIn("../../", result)

    def test_translated_heading_links_follow_english_titles(self):
        source = self.root / "README.md"
        target = self.output / "README.md"
        source.write_text("# 中文指南\n\n[Section](FAQ.md#_4、配置)\n")
        (self.root / "FAQ.md").write_text("# 4、配置\n")
        (self.output / "FAQ.md").write_text("# 4. Configuration\n")
        text = "# English guide\n\n[Section](FAQ.md#_4、配置)\n"
        result = docs.repair_local_links(text, target, self.root, source_path=source,
                                        translated_files={"README.md", "FAQ.md"})
        self.assertIn("FAQ.md#_4-configuration", result)
        target.write_text(result)
        docs.validate_document(source, target, self.root)

    def test_same_page_heading_links_and_duplicate_titles_remain_valid(self):
        source = self.root / "README.md"
        target = self.output / "README.md"
        source.write_text("# 中文指南\n\n[Again](#中文指南-1)\n\n# 中文指南\n")
        target.write_text("# English guide\n\n[Again](#中文指南-1)\n\n# English guide\n")
        result = docs.repair_local_links(target.read_text(), target, self.root,
                                        source_path=source, translated_files={"README.md"})
        self.assertIn("[Again](#english-guide-1)", result)
        target.write_text(result)
        docs.validate_document(source, target, self.root)

    def test_cached_heading_links_can_be_rebased_without_an_api_call(self):
        source = self.root / "README.md"
        target = self.output / "README.md"
        (self.root / "FAQ.md").write_text("# 配置\n")
        (self.output / "FAQ.md").write_text("# New configuration\n")
        source.write_text("# 指南\n\n[Section](FAQ.md#配置)\n")
        target.write_text("# Guide\n\n[Section](FAQ.md#configuration)\n")
        result = docs.repair_local_links(target.read_text(), target, self.root,
                                        translated_files={"README.md", "FAQ.md"},
                                        previous_anchors={"FAQ.md": {"配置": "configuration"}})
        self.assertIn("FAQ.md#new-configuration", result)
        target.write_text(result)
        docs.validate_document(source, target, self.root)

    def test_incremental_sync_translates_new_and_changed_files_only(self):
        files = ["README.md", "_sidebar.md", "项目/指南.md"]
        for name in files:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("# 文档\n\nText.\n")
        readme = self.root / "README.md"
        readme.write_text(docs.apply_language_switch(readme.read_text(), "zh", readme,
                                                   self.output / "README.md"))
        calls = []

        async def translate(text, language, options):
            calls.append(Path(options["source_path"]).name)
            return text.replace("# 文档", "# Guide")

        with patch.object(docs, "discover_documents", side_effect=lambda root: tuple(files)), \
             patch.object(docs, "configure_deepseek"), \
             patch("co_op_translator.api.translate_markdown_content", side_effect=translate):
            docs.sync_docs(self.root)
            self.assertCountEqual(calls, ["README.md", "_sidebar.md", "指南.md"])
            calls.clear()
            before = (self.output / "项目/指南.md").stat().st_mtime_ns
            docs.sync_docs(self.root)
            self.assertEqual(calls, [])
            self.assertEqual((self.output / "项目/指南.md").stat().st_mtime_ns, before)
            readme.write_text(readme.read_text() + "\nUpdated.\n")
            docs.sync_docs(self.root)
            self.assertEqual(calls, ["README.md"])
            calls.clear()
            files.append("New.md")
            (self.root / "New.md").write_text("# 文档\n")
            docs.sync_docs(self.root)
            self.assertEqual(calls, ["New.md"])
            files.remove("New.md")
            (self.root / "New.md").unlink()
            calls.clear()
            docs.sync_docs(self.root)
            self.assertEqual(calls, [])
            self.assertFalse((self.output / "New.md").exists())
            self.assertNotIn("New.md", json.loads((self.output / docs.METADATA).read_text()))


if __name__ == "__main__":
    unittest.main()
