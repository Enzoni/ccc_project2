module.exports = {
  lintOnSave: false,
  configureWebpack: {
    devtool: 'source-map'
  },
  chainWebpack: config => {

  },
  productionSourceMap: false,
  publicPath: process.env.NODE_ENV === 'production' ? './' : '/',
  devServer: { 
    disableHostCheck: true,
    host: '0.0.0.0',
    port: 80,
    proxy: {
      '/api': {
        target: 'http://10.8.57.220:5000',
        ws: true,
        changeOrigin: true,
        secure: false
      }
    }
  },
}
