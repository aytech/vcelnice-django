import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { RouterModule } from '@angular/router';

import { PageNotFoundComponent } from './page-not-found.component';

describe('PageNotFoundComponent', () => {
  let component: PageNotFoundComponent;
  let fixture: ComponentFixture<PageNotFoundComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ PageNotFoundComponent ],
      imports: [ RouterModule.forRoot([]) ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PageNotFoundComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('fills the available page with an accessible image-backed error view', () => {
    const element: HTMLElement = fixture.nativeElement;
    const section = element.querySelector<HTMLElement>('.not-found');
    const image = element.querySelector<HTMLImageElement>('.not-found__image');
    const heading = element.querySelector<HTMLHeadingElement>('h1');

    expect(section?.getAttribute('aria-labelledby')).toBe('not-found-title');
    expect(heading?.id).toBe('not-found-title');
    expect(image?.getAttribute('src')).toBe('/assets/error.jpg');
    expect(image?.getAttribute('alt')).toBe('');
    expect(getComputedStyle(image!).objectFit).toBe('cover');
    expect(element.querySelector('video')).toBeNull();
  });

  it('links back to the landing page', () => {
    const link = fixture.nativeElement.querySelector('.not-found__action') as HTMLAnchorElement;
    const url = new URL(link.href);

    expect(url.pathname).toBe('/');
    expect(link.textContent).toContain('Zpět na úvodní stránku');
  });
});
