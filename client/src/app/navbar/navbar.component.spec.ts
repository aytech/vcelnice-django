import { ApplicationRef } from '@angular/core'
import { provideHttpClient } from '@angular/common/http'
import {
  HttpTestingController,
  provideHttpClientTesting
} from '@angular/common/http/testing'
import { ComponentFixture, TestBed } from '@angular/core/testing'
import { RouterModule } from '@angular/router'
import { ApiConstants } from '@config'
import { LanguageService } from '@services'
import { NavbarComponent } from './navbar.component'

describe('NavbarComponent', () => {
  let fixture: ComponentFixture<NavbarComponent>
  let languageService: LanguageService
  let httpTesting: HttpTestingController

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [NavbarComponent],
      imports: [RouterModule.forRoot([])],
      providers: [
        LanguageService,
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    }).compileComponents()

    languageService = TestBed.inject(LanguageService)
    httpTesting = TestBed.inject(HttpTestingController)
    fixture = TestBed.createComponent(NavbarComponent)
    fixture.autoDetectChanges()
  })

  afterEach(() => {
    httpTesting.verify()
  })

  it('renders translated navigation when the language signals update', async () => {
    expect(navLabels()).toContain('Domů')

    languageService.setLanguage('en')
    httpTesting.expectOne({
      method: 'GET',
      url: `${ApiConstants.GET_CULTURES}?locale=en`
    }).flush({home: 'Home'})

    await TestBed.inject(ApplicationRef).whenStable()

    expect(navLabels()).toContain('Home')
    expect(fixture.nativeElement.querySelector('a.nav-link')?.getAttribute('href'))
      .toContain('locale=en')
  })

  it('links Region immediately after Home and before Novinky', () => {
    const links = navLinks()

    expect(links.slice(0, 3).map(link => link.textContent?.trim()))
      .toEqual(['Domů', 'Region', 'Novinky'])
    expect(links[1].getAttribute('href')).toContain('locale=cs')
    expect(links[1].getAttribute('href')).toContain('#region')
    expect(links[2].getAttribute('href')).toContain('#novinky')
  })

  function navLabels(): string[] {
    return navLinks().map(link => link.textContent?.trim() ?? '')
  }

  function navLinks(): HTMLAnchorElement[] {
    const element: HTMLElement = fixture.nativeElement

    return Array.from(element.querySelectorAll<HTMLAnchorElement>('a.nav-link'))
  }
})
