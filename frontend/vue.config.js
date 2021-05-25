module.exports = {
  lintOnSave: false,
  configureWebpack: {
    devtool: 'source-map'
  },
  productionSourceMap: false,
  publicPath: process.env.NODE_ENV === 'production' ? './' : '/',
  devServer: { 
    disableHostCheck: true,
    host: '0.0.0.0',
    port: 80,
    proxy: {
      '/api': {
        target: 'http://0.0.0.0:5000',
        ws: true,
        changeOrigin: true,
        secure: false
      }
    }
  },
}
