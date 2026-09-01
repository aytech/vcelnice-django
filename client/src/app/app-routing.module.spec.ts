import { TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';

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
});
