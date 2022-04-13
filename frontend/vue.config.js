const path = require('path')
const CopyWebpackPlugin = require('copy-webpack-plugin')

module.exports = {
  publicPath: '/',
  lintOnSave: false,
  pwa: {
    workboxPluginMode: 'GenerateSW',
      workboxOptions: {
          skipWaiting: true
      }
  },
  configureWebpack: {
    plugins: [
      new CopyWebpackPlugin([{
        from: path.join(__dirname, "./docs"),
        to: path.join(__dirname, "dist/docs"),
        toType: "dir"
      }
    ])]
  }
}