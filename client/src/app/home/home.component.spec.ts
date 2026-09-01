import { ApplicationRef, Component } from '@angular/core';
import { provideHttpClient } from '@angular/common/http';
import {
  HttpTestingController,
  provideHttpClientTesting
} from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ApiConstants } from '@config';
import { Home } from '@interfaces';
import { HomeService } from '@services';
import { HomeComponent } from './home.component';

@Component({
  selector: 'app-region',
  template: '<div class="region-stub">Region</div>',
  standalone: false
})
class RegionStubComponent { }

@Component({
  selector: 'app-news',
  template: '<div class="news-stub">Novinky</div>',
  standalone: false
})
class NewsStubComponent { }

describe('HomeComponent', () => {
  const home: Home = {
    id: 1,
    title: 'Včelnice Rudná',
    text: '<p>Poctivý med přímo od včelaře.</p>',
    icon: '/media/home.jpg'
  };
  let fixture: ComponentFixture<HomeComponent>;
  let component: HomeComponent;
  let httpTesting: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [HomeComponent, RegionStubComponent, NewsStubComponent],
      providers: [
        HomeService,
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

  it('shows the loading indicator while the home request is pending', async () => {
    const request = expectHomeRequest();

    expect(component.homeResource.isLoading()).toBeTrue();
    expect(fixture.nativeElement.querySelector('.spinner')).not.toBeNull();

    request.flush(home);
    await stabilizeFixture();
  });

  it('renders Region between the main content and Novinky', async () => {
    const request = expectHomeRequest();

    request.flush(home);
    await stabilizeFixture();

    const element: HTMLElement = fixture.nativeElement;
    const region = element.querySelector<HTMLElement>('#region');
    const news = element.querySelector<HTMLElement>('#novinky');

    expect(component.homeResource.hasValue()).toBeTrue();
    expect(component.homeResource.isLoading()).toBeFalse();
    expect(element.querySelector('h1')?.textContent?.trim()).toBe(home.title);
    expect(element.querySelector('.main-text')?.textContent).toContain(
      'Poctivý med přímo od včelaře.'
    );
    expect(region?.previousElementSibling?.classList.contains('container')).toBeTrue();
    expect(region?.nextElementSibling).toBe(news);
    expect(region?.querySelector('.region-stub')).not.toBeNull();
    expect(news?.querySelector('.news-stub')).not.toBeNull();
    expect(element.querySelector('.spinner')).toBeNull();
    expect(element.querySelector('[role="alert"]')).toBeNull();
  });

  it('stops loading and renders an error when a request fails', async () => {
    const request = expectHomeRequest();

    request.flush('Request failed', {
      status: 500,
      statusText: 'Internal Server Error'
    });
    await stabilizeFixture();

    const element: HTMLElement = fixture.nativeElement;

    expect(component.homeResource.isLoading()).toBeFalse();
    expect(component.homeResource.error()).toBeTruthy();
    expect(element.querySelector('.spinner')).toBeNull();
    expect(element.querySelector('[role="alert"]')?.textContent).toContain(
      'neočekávaná chyba'
    );
  });

  function expectHomeRequest() {
    return httpTesting.expectOne({
      method: 'GET',
      url: ApiConstants.GET_HOME
    });
  }

  async function stabilizeFixture(): Promise<void> {
    await TestBed.inject(ApplicationRef).whenStable();
  }
});
