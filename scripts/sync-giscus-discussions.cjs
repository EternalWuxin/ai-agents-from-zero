const { execFileSync } = require("node:child_process");
const fs = require("node:fs");
const path = require("node:path");

const DEFAULT_REPOSITORY = "didilili/ai-agents-from-zero";
const START_MARKER = "  // giscus-discussions:start";
const END_MARKER = "  // giscus-discussions:end";

const DISCUSSIONS_QUERY = `
  query($owner: String!, $name: String!, $after: String) {
    repository(owner: $owner, name: $name) {
      discussions(first: 100, after: $after) {
        nodes {
          number
          title
          createdAt
          comments {
            totalCount
          }
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
  }
`;

function commentCount(discussion) {
  return Number(discussion.comments?.totalCount || 0);
}

function selectDiscussionNumbers(discussions) {
  const groups = new Map();

  for (const discussion of discussions) {
    const title = String(discussion.title || "").trim();
    if (!title) continue;

    const group = groups.get(title) || [];
    group.push(discussion);
    groups.set(title, group);
  }

  const selected = [];
  const duplicates = [];

  for (const [title, group] of groups) {
    group.sort(
      (left, right) =>
        commentCount(right) - commentCount(left) ||
        new Date(left.createdAt).getTime() -
          new Date(right.createdAt).getTime() ||
        left.number - right.number,
    );

    const canonical = group[0];
    selected.push({ title, number: canonical.number });

    if (group.length > 1) {
      duplicates.push({
        title,
        selected: canonical.number,
        skipped: group.slice(1).map((discussion) => discussion.number),
      });
    }
  }

  selected.sort((left, right) => left.number - right.number);
  duplicates.sort((left, right) => left.selected - right.selected);

  return {
    discussionNumbers: Object.fromEntries(
      selected.map(({ title, number }) => [title, number]),
    ),
    duplicates,
  };
}

function replaceDiscussionNumbers(source, discussionNumbers) {
  const start = source.indexOf(START_MARKER);
  const end = source.indexOf(END_MARKER);

  if (start === -1 || end === -1 || end <= start) {
    throw new Error(
      "Could not find the generated giscus discussion map markers",
    );
  }

  const serialized = JSON.stringify(discussionNumbers, null, 2)
    .split("\n")
    .map((line, index) => (index === 0 ? line : `  ${line}`))
    .join("\n");
  const generated = `${START_MARKER}\n  var discussionNumbers = ${serialized};\n${END_MARKER}`;

  return (
    source.slice(0, start) + generated + source.slice(end + END_MARKER.length)
  );
}

function fetchDiscussions(repository = DEFAULT_REPOSITORY) {
  const [owner, name, extra] = repository.split("/");
  if (!owner || !name || extra) {
    throw new Error(`Invalid GitHub repository: ${repository}`);
  }

  const discussions = [];
  let cursor;

  do {
    const args = [
      "api",
      "graphql",
      "-f",
      `query=${DISCUSSIONS_QUERY}`,
      "-f",
      `owner=${owner}`,
      "-f",
      `name=${name}`,
    ];
    if (cursor) args.push("-f", `after=${cursor}`);

    let response;
    try {
      response = JSON.parse(
        execFileSync("gh", args, {
          encoding: "utf8",
          stdio: ["ignore", "pipe", "pipe"],
        }),
      );
    } catch (error) {
      const detail = error.stderr?.toString().trim() || error.message;
      throw new Error(`Could not read GitHub Discussions with gh: ${detail}`);
    }

    const connection = response.data?.repository?.discussions;
    if (!connection) {
      throw new Error(`GitHub returned no Discussions data for ${repository}`);
    }

    discussions.push(...connection.nodes);
    cursor = connection.pageInfo.hasNextPage
      ? connection.pageInfo.endCursor
      : undefined;
  } while (cursor);

  return discussions;
}

function syncDiscussionNumbers() {
  const root = path.resolve(__dirname, "..");
  const pluginPath = path.join(root, "lib/plugins/giscus.js");
  const repository = process.env.GISCUS_REPO || DEFAULT_REPOSITORY;
  const discussions = fetchDiscussions(repository);
  const selection = selectDiscussionNumbers(discussions);
  const source = fs.readFileSync(pluginPath, "utf8");
  const updated = replaceDiscussionNumbers(source, selection.discussionNumbers);

  if (updated !== source) {
    fs.writeFileSync(pluginPath, updated);
  }

  console.log(
    `Synced ${Object.keys(selection.discussionNumbers).length} discussion mappings from ${repository}.`,
  );

  for (const duplicate of selection.duplicates) {
    console.warn(
      `Duplicate title: ${duplicate.title}; selected #${duplicate.selected}, skipped ${duplicate.skipped.map((number) => `#${number}`).join(", ")}.`,
    );
  }
}

module.exports = {
  fetchDiscussions,
  replaceDiscussionNumbers,
  selectDiscussionNumbers,
  syncDiscussionNumbers,
};

if (require.main === module) {
  try {
    syncDiscussionNumbers();
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}
