module.exports = {
  css: {
    sourceMap: true,
  },
  publicPath: '/static/',
  outputDir: '../system/static',
  lintOnSave: false,
  productionSourceMap: false,
  pages: {
    index: {
      entry: 'src/main.js',
      template: 'public/index.html',
      filename: 'index.html',
    },
  },
  runtimeCompiler: true,
  configureWebpack: {
    performance: {
      maxAssetSize: 500000,
    },
    //Necessary to run npm link https://webpack.js.org/configuration/resolve/#resolve-symlinks
    resolve: {
       symlinks: false
    }
  },
  devServer: {
    proxy: 'http://127.0.0.1:8000' // This will tell the dev server to proxy any unknown requests
  },
  transpileDependencies: [
    '@coreui/utils',
    '@coreui/vue'
  ]
};
