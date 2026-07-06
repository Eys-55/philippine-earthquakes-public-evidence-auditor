import { defineConfig } from "astro/config";

export default defineConfig({
  output: "static",
  srcDir: "./tracker-ui/src",
  publicDir: "./tracker-ui/public",
  outDir: "./dist/tracker-ui"
});
