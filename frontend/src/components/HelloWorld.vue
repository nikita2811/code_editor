<template>
  <div ref="container" class="monaco-container"></div>
   <button @click="runCode" class="run-btn">Run</button>
    <pre class="output">{{ output }}</pre>
</template>

<script setup>
/* global monaco */
import { onMounted, ref } from 'vue'

const container = ref(null)
const output = ref('')
let editor = null

onMounted(() => {
  if (!window.require) {
    console.error('Monaco loader not available yet.')
    return
  }
  // Load Monaco globally (assumes it's on window.require)
  window.require.config({ paths: { vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs' } })
   window.require(['vs/editor/editor.main'], () => {
    editor = monaco.editor.create(container.value, {
      value: `"Hello from Monaco!"`,
      language: 'javascript,python',
      theme: 'vs-dark',
    })
  })
})
function runCode() {
  try {
    const code = editor.getValue()
    console.log('Running code:', code)
    const capturedLogs = []

    // Capture console.log
    const originalLog = console.log
    console.log = (...args) => capturedLogs.push(args.join(' '))

    // Run the code
    new Function(code)()

    // Restore console.log and show output
    console.log = originalLog
    output.value = capturedLogs.join('\n') || '[No output]'
  } catch (err) {
    output.value = `Error: ${err.message}`
  }
}
</script>

<style scoped>
.monaco-container {
  height: 500px;
  border: 1px solid #ccc;
}
</style>
