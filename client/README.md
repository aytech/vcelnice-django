# Client

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 1.6.0.

## Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory. Use the `-prod` flag for a production build.

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

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via [Protractor](http://www.protractortest.org/).

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI README](https://github.com/angular/angular-cli/blob/master/README.md).
