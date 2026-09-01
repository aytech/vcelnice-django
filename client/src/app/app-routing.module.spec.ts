import { TestBed } from '@angular/core/testing';
import { ROUTER_CONFIGURATION, Router } from '@angular/router';

import { AppRoutingModule } from './app-routing.module';
import { CertificatesComponent } from './certificates/certificates.component';
import { ContactComponent } from './contact/contact.component';
import { VideoComponent } from './video/video.component';

describe('AppRoutingModule', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [AppRoutingModule]
    });
  });

  it('keeps direct routes for Certifikáty, Kontakt and Video', () => {
    const routes = TestBed.inject(Router).config;

    expect(routes.find(route => route.path === 'certifikaty')?.component).toBe(CertificatesComponent);
    expect(routes.find(route => route.path === 'kontakt')?.component).toBe(ContactComponent);
    expect(routes.find(route => route.path === 'video')?.component).toBe(VideoComponent);
  });

  it('scrolls to sections and returns fragment-free navigation to the top', () => {
    const options = TestBed.inject(ROUTER_CONFIGURATION);

    expect(options.anchorScrolling).toBe('enabled');
    expect(options.scrollPositionRestoration).toBe('enabled');
    expect(options.scrollOffset).toEqual([0, 72]);
  });
});
