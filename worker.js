export default {
  fetch(request, env) {
    const url = new URL(request.url);
    if (/^\/(?:history|incident)\/[^/]+\/?$/.test(url.pathname) || url.pathname === '/rate-limit-exceeded') {
      url.pathname = '/';
      return env.ASSETS.fetch(new Request(url, request));
    }
    return env.ASSETS.fetch(request);
  },
};
