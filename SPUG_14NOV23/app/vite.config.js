import { defineConfig } from 'vite'
import solid from 'vite-plugin-solid'

import { resolve } from 'path';

const root = resolve(__dirname, "src", "pages")
const build = resolve(__dirname, "build")

export default defineConfig({
  plugins: [solid()],
  root: root,
  publicDir: "../public",
  build: {
    target: 'esnext',
    polyfillDynamicImport: false,
      rollupOptions: {
        input: {
            home: resolve(root, "index.html"),
         },
      },
    outDir: build,
  },
})
