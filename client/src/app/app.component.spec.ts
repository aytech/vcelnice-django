import { NO_ERRORS_SCHEMA } from '@angular/core';
import { TestBed, waitForAsync } from '@angular/core/testing';
import { ActivatedRoute } from '@angular/router';
import { AppComponent } from './app.component';
import { LanguageService } from '../services';

describe('AppComponent', () => {
  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [
        AppComponent
      ],
      providers: [
        {
          provide: ActivatedRoute,
          useValue: {
            snapshot: { queryParams: {} },
            queryParams: { subscribe: () => ({ unsubscribe() {} }) }
          }
        },
        {
          provide: LanguageService,
          useValue: { setLanguage: () => {} }
        }
      ],
      schemas: [NO_ERRORS_SCHEMA]
    }).compileComponents();
  }));
  it('should create the app', () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.debugElement.componentInstance;
    expect(app).toBeTruthy();
  });
  it('should render the application shell', () => {
    const fixture = TestBed.createComponent(AppComponent);
    fixture.detectChanges();
    const compiled: HTMLElement = fixture.debugElement.nativeElement;
    const main = compiled.querySelector<HTMLElement>('.app-main');

    expect(compiled.querySelector('app-navbar')).not.toBeNull();
    expect(main).not.toBeNull();
    expect(main?.querySelector('router-outlet')).not.toBeNull();
    expect(compiled.querySelector('app-footer')).not.toBeNull();
    expect(Array.from(compiled.children).map(element => element.tagName)).toEqual([
      'APP-NAVBAR',
      'MAIN',
      'APP-FOOTER'
    ]);
    expect(getComputedStyle(compiled).display).toBe('flex');
    expect(getComputedStyle(compiled).flexDirection).toBe('column');
    expect(getComputedStyle(main!).flexGrow).toBe('1');
  });
});
