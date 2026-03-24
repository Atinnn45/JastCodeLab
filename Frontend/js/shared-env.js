// JastCodeLab — Environment Config
// Auto-detect dev vs production API URL

window.BASE_URL = (location.hostname === 'localhost' || location.hostname === '127.0.0.1')
  ? 'http://127.0.0.1:8000'
  : 'https://jastcodelab-production.up.railway.app';
