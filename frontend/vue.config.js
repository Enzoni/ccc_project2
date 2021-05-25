// ==========================
// COMP90024 Assignment 2
// Team: 38
// City: Melbourne
// Members:
// Ziran Gu (1038782)
// Jueying Wang (1016724)
// Yifei Zhou(980429)
// Jiakai Ni (988303)
// Ziyue Liu (1036109)
// ==========================
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
        target: 'http://172.26.132.206:5000',
        ws: true,
        changeOrigin: true,
        secure: false
      }
    }
  },
}
