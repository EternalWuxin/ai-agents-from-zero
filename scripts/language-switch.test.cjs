const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");

const pluginPath = path.resolve(__dirname, "../lib/plugins/language-switch.js");
function plugin() {
  assert.ok(
    fs.existsSync(pluginPath),
    "website language switch is implemented",
  );
  return require(pluginPath);
}

const chapter = "1-1-大模型认知与工程概览.md";
const metadata = {
  "README.md": { language_code: "en" },
  [chapter]: { language_code: "en" },
};

test("both homepage URLs switch to the corresponding language homepage", () => {
  const { switchTarget } = plugin();
  assert.equal(switchTarget("/", "en", metadata), "#/translations/en/");
  assert.equal(
    switchTarget("/README.md", "en", metadata),
    "#/translations/en/",
  );
  assert.equal(switchTarget("/translations/en/", "zh", metadata), "#/");
  assert.equal(switchTarget("/translations/en/README", "zh", metadata), "#/");
});

test("switching a translated chapter preserves the page and handles encoded paths", () => {
  const { switchTarget } = plugin();
  const source = "/" + encodeURIComponent(chapter.replace(/\.md$/, ""));
  assert.equal(
    switchTarget(source + "?id=中文标题", "en", metadata),
    "#/translations/en/" + encodeURIComponent(chapter),
  );
  assert.equal(
    switchTarget(
      "/translations/en/" + encodeURIComponent(chapter),
      "zh",
      metadata,
    ),
    "#/" + encodeURIComponent(chapter),
  );
});

test("an untranslated page stays in Chinese instead of navigating to a missing file", () => {
  const { switchTarget } = plugin();
  assert.equal(switchTarget("/1-2-提示词工程基础", "en", metadata), null);
  assert.equal(switchTarget("/1-2-提示词工程基础", "en", {}), null);
  assert.equal(
    switchTarget("/1-2-提示词工程基础", "zh", metadata),
    "#/" + encodeURIComponent("1-2-提示词工程基础.md"),
  );
});

test("nested source paths and special characters remain valid routes", () => {
  const { switchTarget } = plugin();
  const name = "案例/Coze&Dify 入门.md";
  const manifest = { [name]: { language_code: "en" } };
  assert.equal(
    switchTarget("/" + name, "en", manifest),
    "#/translations/en/" + name.split("/").map(encodeURIComponent).join("/"),
  );
  assert.equal(
    switchTarget("/" + name, "en", { [name]: { language_code: "fr" } }),
    null,
  );
});
