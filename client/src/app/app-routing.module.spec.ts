import { TestBed } from '@angular/core/testing';
import { ROUTER_CONFIGURATION, Router } from '@angular/router';

import { AppRoutingModule } from './app-routing.module';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { PrivacyComponent } from './privacy/privacy.component';

describe('AppRoutingModule', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [AppRoutingModule]
    });
  });

  it('keeps the direct privacy route available', () => {
    const routes = TestBed.inject(Router).config;

    expect(routes.find(route => route.path === 'privacy')?.component).toBe(PrivacyComponent);
  });

  it('removes standalone routes for Ceník, Certifikáty, Video and Kontakt', () => {
    const routes = TestBed.inject(Router).config;

    expect(routes.some(route => route.path === 'cenik')).toBeFalse();
    expect(routes.some(route => route.path === 'certifikaty')).toBeFalse();
    expect(routes.some(route => route.path === 'video')).toBeFalse();
    expect(routes.some(route => route.path === 'kontakt')).toBeFalse();
    expect(routes.find(route => route.path === '**')?.component).toBe(PageNotFoundComponent);
  });

  it('scrolls to sections and returns fragment-free navigation to the top', () => {
    const options = TestBed.inject(ROUTER_CONFIGURATION);

    expect(options.anchorScrolling).toBe('enabled');
    expect(options.scrollPositionRestoration).toBe('enabled');
    expect(options.scrollOffset).toEqual([0, 72]);
  });
});
