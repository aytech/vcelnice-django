import { NO_ERRORS_SCHEMA } from '@angular/core';
import { TestBed, waitForAsync } from '@angular/core/testing';
import { ActivatedRoute, Params } from '@angular/router';
import { Subject } from 'rxjs';
import { AppComponent } from './app.component';
import { LanguageService } from '../services';

describe('AppComponent', () => {
  let queryParams: Subject<Params>;
  let route: { snapshot: { queryParams: Params }, queryParams: Subject<Params> };
  let languageService: jasmine.SpyObj<LanguageService>;

  beforeEach(waitForAsync(() => {
    queryParams = new Subject<Params>();
    route = {
      snapshot: { queryParams: {} },
      queryParams
    };
    languageService = jasmine.createSpyObj<LanguageService>(
      'LanguageService',
      ['setLanguage']
    );

    TestBed.configureTestingModule({
      declarations: [
        AppComponent
      ],
      providers: [
        {
          provide: ActivatedRoute,
          useValue: route
        },
        {
          provide: LanguageService,
          useValue: languageService
        }
      ],
      schemas: [NO_ERRORS_SCHEMA]
    }).compileComponents();
  }));
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

  it('uses the locale from the initial URL', () => {
    route.snapshot.queryParams = { locale: 'en' };

    const fixture = TestBed.createComponent(AppComponent);
    fixture.detectChanges();

    expect(languageService.setLanguage).toHaveBeenCalledOnceWith('en');
  });

  it('updates the language when URL query parameters change', () => {
    const fixture = TestBed.createComponent(AppComponent);
    fixture.detectChanges();

    queryParams.next({});
    expect(languageService.setLanguage).not.toHaveBeenCalled();

    queryParams.next({ locale: 'en' });
    expect(languageService.setLanguage).toHaveBeenCalledOnceWith('en');
  });
});
