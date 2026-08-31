import { ApplicationRef, Component } from '@angular/core';
import { provideHttpClient } from '@angular/common/http';
import {
  HttpTestingController,
  provideHttpClientTesting,
  TestRequest
} from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ApiConstants } from '@config';
import { Article, Home } from '@interfaces';
import { HomeService, NewsService } from '@services';
import { HomeComponent } from './home.component';

@Component({
  selector: 'app-modal',
  template: '',
  standalone: false
})
class ModalStubComponent {
  open(_title: string, _body: string): void { }
}

describe('HomeComponent', () => {
  const home: Home = {
    id: 1,
    title: 'Včelnice Rudná',
    text: '<p>Poctivý med přímo od včelaře.</p>',
    icon: '/media/home.jpg'
  };
  const articles: Article[] = Array.from({length: 5}, (_, index) => ({
    id: index + 1,
    title: `Novinka ${index + 1}`,
    text: `Text novinky ${index + 1}`,
    icon: '',
    created: '2026-08-31T00:00:00Z',
    updated: '2026-08-31T00:00:00Z'
  }));

  let fixture: ComponentFixture<HomeComponent>;
  let component: HomeComponent;
  let httpTesting: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [HomeComponent, ModalStubComponent],
      providers: [
        HomeService,
        NewsService,
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    }).compileComponents();

    httpTesting = TestBed.inject(HttpTestingController);
    fixture = TestBed.createComponent(HomeComponent);
    component = fixture.componentInstance;
    fixture.autoDetectChanges();
    TestBed.tick();
  });

  afterEach(() => {
    httpTesting.verify();
  });

  it('shows the loading indicator while both requests are pending', async () => {
    const requests = expectPageRequests();

    expect(component.pageResource.isLoading()).toBeTrue();
    expect(fixture.nativeElement.querySelector('.spinner')).not.toBeNull();

    requests.home.flush(home);
    requests.news.flush(articles);
    await stabilizeFixture();
  });

  it('renders the home text and only the four newest cards after both requests complete', async () => {
    const requests = expectPageRequests();

    requests.home.flush(home);
    requests.news.flush(articles);
    await stabilizeFixture();

    const element: HTMLElement = fixture.nativeElement;
    const cardTitles = Array.from(
      element.querySelectorAll<HTMLElement>('.card-title')
    ).map(title => title.textContent?.trim());

    expect(component.pageResource.hasValue()).toBeTrue();
    expect(component.pageResource.isLoading()).toBeFalse();
    expect(element.querySelector('h1')?.textContent?.trim()).toBe(home.title);
    expect(element.querySelector('.main-text')?.textContent).toContain(
      'Poctivý med přímo od včelaře.'
    );
    expect(cardTitles).toEqual(articles.slice(0, 4).map(article => article.title));
    expect(element.querySelector('.spinner')).toBeNull();
    expect(element.querySelector('[role="alert"]')).toBeNull();
  });

  it('stops loading and renders an error when a request fails', async () => {
    const requests = expectPageRequests();

    requests.news.flush(articles);
    requests.home.flush('Request failed', {
      status: 500,
      statusText: 'Internal Server Error'
    });
    await stabilizeFixture();

    const element: HTMLElement = fixture.nativeElement;

    expect(component.pageResource.isLoading()).toBeFalse();
    expect(component.pageResource.error()).toBeTruthy();
    expect(element.querySelector('.spinner')).toBeNull();
    expect(element.querySelector('[role="alert"]')?.textContent).toContain(
      'neočekávaná chyba'
    );
  });

  function expectPageRequests(): {home: TestRequest; news: TestRequest} {
    const homeRequest = httpTesting.expectOne({
      method: 'GET',
      url: ApiConstants.GET_HOME
    });
    const newsRequest = httpTesting.expectOne({
      method: 'GET',
      url: ApiConstants.GET_NEWS
    });

    return {home: homeRequest, news: newsRequest};
  }

  async function stabilizeFixture(): Promise<void> {
    await TestBed.inject(ApplicationRef).whenStable();
  }
});
