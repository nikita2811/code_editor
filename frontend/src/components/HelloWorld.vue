<template>
  <div class="p-4 space-y-4">
    <div class="flex gap-4 items-center">
      <select v-model="language" class="border px-2 py-1 rounded">
        <option value="python">Python</option>
        <option value="javascript">JavaScript</option>
        <option value="php">PHP</option>
      </select>
      <button @click="runCode" class="bg-blue-600 text-white px-4 py-2 rounded">Run Code</button>
    </div>

    <div ref="editorContainer" class="editor"/>

    <div class="mt-4 bg-black text-green-400 p-4 rounded whitespace-pre-wrap min-h-[100px]">
      <strong>Output:</strong>
      <div>{{ output || '[no output]' }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

/* global monaco */

const editorContainer = ref(null)
let editorInstance = null
const output = ref('')
const language = ref('python')

onMounted(() => {
  // Load Monaco via CDN
  if (!window.require) {
    console.error("Monaco loader not found")
    return
  }

  window.require.config({
    paths: { vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs' }
  })

  window.require(['vs/editor/editor.main'], () => {
    editorInstance = monaco.editor.create(editorContainer.value, {
      value: getDefaultCode(language.value),
      language: language.value,
      theme: 'vs-dark'
    })
  })
})

function getDefaultCode(lang) {
  switch (lang) {
    case 'python':
      return `print("Hello from Python")`
    case 'javascript':
      return `console.log("Hello from JavaScript")`
    case 'php':
      return `<?php echo "Hello from PHP"; ?>`
  }
}

function runCode() {
  const code = editorInstance.getValue()
  output.value = '[running...]'

  axios.post('http://localhost:8000/editor/code/', {
    code,
  })
    .then(res => {
      const { stdout, stderr } = res.data
      output.value = stdout || stderr || '[no output]'
    })
    .catch(err => {
      output.value = `Error: ${err.response?.data?.error || err.message}`
    })
}
</script>

<style scoped>
select {
  min-width: 150px;
}
.editor {
  height: 300px;
  border: 1px solid #ccc;
}
</style>
