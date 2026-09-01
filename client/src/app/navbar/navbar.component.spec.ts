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

  it('links Ceník to its landing-page section and keeps the expected navigation order', () => {
    const links = navLinks()
    const priceUrl = new URL(linkByLabel('Ceník').href)
    const photoUrl = new URL(linkByLabel('Foto').href)
    const recipesUrl = new URL(linkByLabel('Recepty').href)
    const contactUrl = new URL(linkByLabel('Kontakt').href)

    expect(links.map(link => link.textContent?.trim()))
      .toEqual(['Domů', 'Ceník', 'Region', 'Novinky', 'Foto', 'Recepty', 'Kontakt'])
    expect(navLabels()).not.toContain('Video')
    expect(navLabels()).not.toContain('Certifikáty')
    expect(priceUrl.pathname).toBe('/')
    expect(priceUrl.searchParams.get('locale')).toBe('cs')
    expect(priceUrl.hash).toBe('#cenik')
    expect(photoUrl.pathname).toBe('/')
    expect(photoUrl.searchParams.get('locale')).toBe('cs')
    expect(photoUrl.hash).toBe('#foto')
    expect(recipesUrl.pathname).toBe('/')
    expect(recipesUrl.searchParams.get('locale')).toBe('cs')
    expect(recipesUrl.hash).toBe('#recepty')
    expect(contactUrl.pathname).toBe('/')
    expect(contactUrl.searchParams.get('locale')).toBe('cs')
    expect(contactUrl.hash).toBe('#kontakt')
  })

  it('updates link states without a visual transition', () => {
    navLinks().forEach(link => {
      const styles = getComputedStyle(link)

      expect(styles.transitionProperty).toBe('none')
      expect(styles.transitionDuration).toBe('0s')
    })
  })

  function navLabels(): string[] {
    return navLinks().map(link => link.textContent?.trim() ?? '')
  }

  function linkByLabel(label: string): HTMLAnchorElement {
    const link = navLinks().find(candidate => candidate.textContent?.trim() === label)

    if (!link) {
      throw new Error(`Navigation link not found: ${label}`)
    }

    return link
  }

  function navLinks(): HTMLAnchorElement[] {
    const element: HTMLElement = fixture.nativeElement

    return Array.from(element.querySelectorAll<HTMLAnchorElement>('a.nav-link'))
  }
})
