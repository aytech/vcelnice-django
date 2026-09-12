# Client

Angular 22 application using Angular's esbuild application builder and Vite development server.

Use Node.js 24.15 or newer within the 24.x LTS line, then run `npm ci` to install
the locked dependencies. Node.js 22.22.0 is below this Angular version's minimum.

## Development server

Run `npm start` for the development server at `http://localhost:4200/`. It uses
the development build configuration and reloads when source files change.
`proxy.conf.json` targets the Docker backend at `http://api:8888`; when running
Django outside Docker, pass a separate proxy configuration with the local backend
address. Keep the explicit `/api/**` and `/media/**` patterns to cover nested
API and media paths consistently.

The Docker development setup keeps dependencies in a named volume and skips
installation when Angular CLI is already present. After pulling dependency
changes, stop the UI service and run `npm ci` in that service's volume before
starting it again; restarting alone does not refresh packages.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `npm run build` for a production build, or
`npm run ng -- build --configuration development` for an unoptimized development build.

All build targets use `@angular/build`; Webpack and its Karma plugin are no
longer required. The Angular framework and CLI versions are unchanged by this
builder migration.

`outputPath` deliberately uses `{ "base": "dist", "browser": "" }`: Django's
static-file settings and the root `build.sh` expect `dist/index.html` and bundles
directly in `dist`, not `dist/browser`. The packaging script rewrites the HTML's
bundle and preload links to `/assets/`. Lazy JavaScript chunks resolve relative
to those bundles, and generated font resources are stored in `dist/media`.
Keep `<base href="/">` so application routes and section links still use the site
root. No server-side rendering or prerendering is enabled.

## Media lightboxes

Foto, Video and the Home/Contact map links use GLightbox 3.3.1, loaded on demand
through `LightboxService`. Its stylesheet is included in both build and test
configuration. Bootstrap's JavaScript bundle is still needed for the mobile menu;
Fancybox and jQuery are no longer used by this Angular app.

`src/types/glightbox.d.ts` describes the small distribution API we use because
3.3.1's root declarations fail strict TypeScript checking. Review this compatibility
definition when upgrading GLightbox; do not disable project-wide library checking.

- Foto renders only eight previews but passes the complete API photo collection
  to the viewer. There is no thumbnail strip inside GLightbox.
- YouTube and maps use external iframe slides. This preserves native player/map
  controls without Plyr's extra dependencies and early-close polling issues.
  Third-party embeds load only after an ordinary click. Modified clicks keep
  following the original image, YouTube or Google Maps link.
- Preserve `SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"` in Django
  production settings: YouTube needs the embedding site's referrer. The viewer
  explicitly applies this policy to its iframes too.
- Captions are treated as plain text. The shared service owns URL validation,
  Czech controls, keyboard navigation, focus restoration and route-change cleanup.
  If the lazy-loaded viewer cannot load, the original URL opens in the current tab.

After deployment, check photo navigation beyond the eighth image, both map links,
YouTube playback/fullscreen, early close/reopen, Ctrl/Cmd-click, Escape/Tab, mobile
swiping and the Bootstrap menu. Existing section fragments must stay unchanged.

## Running unit tests

Run `npm test` to execute the existing Jasmine tests in headless Chrome via
[Karma](https://karma-runner.github.io), now bundled with `@angular/build:karma`.
Chrome must be installed, or `CHROME_BIN` must point to a compatible Chromium
binary. Run `npm test -- --code-coverage` to generate HTML and LCOV reports in
`coverage/` using `karma-coverage`. The builder's optional
`istanbul-lib-instrument` peer is installed explicitly for coverage instrumentation.

## Running end-to-end tests

The legacy `e2e/` files and Protractor configuration are retained for reference,
but no end-to-end test runner or Angular target is configured. `ng e2e` is not
currently supported.

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI README](https://github.com/angular/angular-cli/blob/master/README.md).
