import { TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';

import { AppRoutingModule } from './app-routing.module';
import { ContactComponent } from './contact/contact.component';
import { VideoComponent } from './video/video.component';

describe('AppRoutingModule', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [AppRoutingModule]
    });
  });

  it('keeps direct routes for the hidden Kontakt and Video pages', () => {
    const routes = TestBed.inject(Router).config;

    expect(routes.find(route => route.path === 'kontakt')?.component).toBe(ContactComponent);
    expect(routes.find(route => route.path === 'video')?.component).toBe(VideoComponent);
  });
});
