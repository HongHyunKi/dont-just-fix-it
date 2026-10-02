// File preservation check; browser behavior is covered by the real capture script.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const vm = require('node:vm');
const script = path.resolve(__dirname, '../validation/ux/docs/issue/assets/profile-save-copy/capture.cjs');
const root = fs.mkdtempSync(path.join(os.tmpdir(), 'djfi-capture-test-'));

async function capture(fail) {
  let state, tabs, evaluations, closed = false;
  const page = {
    goto: async url => { state = url.endsWith('/before.html') ? '확인' : '변경사항 저장'; tabs = 0; evaluations = 0; },
    locator: () => ({ innerText: async () => state }),
    getByLabel: () => ({ inputValue: async () => '홍길동' }),
    screenshot: async ({path: file}) => { fs.writeFileSync(file, 'test image'); },
    keyboard: { press: async key => { if (key === 'Tab') tabs++; } },
    evaluate: async () => {
      if (++evaluations < 3) return tabs === 1 ? 'INPUT' : 'BUTTON';
      return fail; // Force the overflow assertion to fail after writing a screenshot.
    },
  };
  const browser = {
    version: async () => 'test',
    newContext: async () => ({newPage: async () => page, close: async () => {}}),
    close: async () => { closed = true; },
  };
  const processStub = {argv: ['node', script, root], exitCode: 0};
  await vm.runInNewContext(fs.readFileSync(script, 'utf8'), {
    __dirname: path.dirname(script), process: processStub,
    console: {log() {}, error() {}},
    require: name => name === 'playwright' ? {chromium: {launch: async () => browser}}
      : name === 'playwright/package.json' ? {version: 'test'} : require(name),
  });
  assert.equal(processStub.exitCode, fail ? 1 : 0);
  assert.equal(closed, true);
}

(async () => {
  const files = fs.readdirSync(path.dirname(script)).filter(name => /\.(png|json)$/.test(name));
  const original = files.map(name => fs.readFileSync(path.join(path.dirname(script), name)));
  try {
    await capture(false);
    const first = path.join(root, fs.readdirSync(root)[0]);
    const evidence = fs.readFileSync(path.join(first, 'evidence.json'));
    assert.equal(JSON.parse(evidence).conditions.length, 4);
    await capture(false);
    await capture(true);
    const runs = fs.readdirSync(root).map(name => path.join(root, name));
    assert.equal(runs.length, 3);
    assert.equal(runs.filter(dir => fs.existsSync(path.join(dir, 'evidence.json'))).length, 2);
    assert.deepEqual(fs.readFileSync(path.join(first, 'evidence.json')), evidence);
    files.forEach((name, i) => assert.deepEqual(fs.readFileSync(path.join(path.dirname(script), name)), original[i]));
    console.log('PASS: separate capture runs, incomplete evidence, original files preserved');
  } finally { fs.rmSync(root, {recursive: true, force: true}); }
})().catch(error => { console.error(error); process.exitCode = 1; });
