import { constants as fsConstants } from "node:fs";
import fs from "node:fs/promises";
import path from "node:path";
import { createHash } from "node:crypto";

const requestedSource = process.env.SLIDES_SOURCE;
const source = path.resolve(
  requestedSource || "slides/thesis-slides-v0.9.pptx",
);
const canonicalV09Sha256 =
  "467fc283fed0cca02fa4490f48fb17b6340165919141fbc094edfac96b8b4e86";
const requestedOutput = process.env.SLIDES_OUTPUT;

if (!requestedOutput) {
  throw new Error(
    "Set SLIDES_OUTPUT to a new version, for example " +
      "slides/thesis-slides-v0.91.pptx.",
  );
}

const output = path.resolve(requestedOutput);
if (source === output) {
  throw new Error("Source and output must be different files.");
}
if (path.extname(source).toLowerCase() !== ".pptx") {
  throw new Error(`Source must be a .pptx file: ${source}`);
}
if (path.extname(output).toLowerCase() !== ".pptx") {
  throw new Error(`Output must be a .pptx file: ${output}`);
}

const sourceStat = await fs.stat(source);
if (!sourceStat.isFile()) {
  throw new Error(`Source is not a regular file: ${source}`);
}

async function sha256(file) {
  return createHash("sha256").update(await fs.readFile(file)).digest("hex");
}

const sourceHeader = (await fs.readFile(source)).subarray(0, 4);
if (sourceHeader.toString("binary") !== "PK\u0003\u0004") {
  throw new Error(`Source does not have a valid PPTX/ZIP signature: ${source}`);
}

const sourceHash = await sha256(source);
if (!requestedSource && sourceHash !== canonicalV09Sha256) {
  throw new Error(
    "The default v0.9 source does not match the reviewed canonical SHA-256.",
  );
}

try {
  await fs.copyFile(source, output, fsConstants.COPYFILE_EXCL);
} catch (error) {
  if (error?.code === "EEXIST") {
    throw new Error(`Refusing to overwrite existing output: ${output}`, {
      cause: error,
    });
  }
  throw error;
}

const outputHash = await sha256(output);
if (sourceHash !== outputHash) {
  await fs.unlink(output);
  throw new Error("Copied file failed SHA-256 verification; output was removed.");
}

console.log(
  `Created an exact, non-overwriting branch:\n${source}\n→ ${output}\n` +
    `SHA-256: ${outputHash}`,
);
