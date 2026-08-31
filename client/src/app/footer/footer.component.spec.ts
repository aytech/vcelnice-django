import { ApplicationRef } from '@angular/core'
import { provideHttpClient } from '@angular/common/http'
import {
  HttpTestingController,
  provideHttpClientTesting
} from '@angular/common/http/testing'
import { ComponentFixture, TestBed } from '@angular/core/testing'
import { ApiConstants } from '@config'
import { LanguageService } from '@services'
import { FooterComponent } from './footer.component'

describe('FooterComponent', () => {
  let fixture: ComponentFixture<FooterComponent>
  let languageService: LanguageService
  let httpTesting: HttpTestingController

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [FooterComponent],
      providers: [
        LanguageService,
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    }).compileComponents()

    languageService = TestBed.inject(LanguageService)
    httpTesting = TestBed.inject(HttpTestingController)
    fixture = TestBed.createComponent(FooterComponent)
    fixture.autoDetectChanges()
  })

  afterEach(() => {
    httpTesting.verify()
  })

  it('updates the badge image when the locale signal changes', async () => {
    expect(badgeImage().getAttribute('src')).toContain('google-play-badge-cs.png')

    languageService.setLanguage('en')
    httpTesting.expectOne({
      method: 'GET',
      url: `${ApiConstants.GET_CULTURES}?locale=en`
    }).flush({})

    await TestBed.inject(ApplicationRef).whenStable()

    expect(badgeImage().getAttribute('src')).toContain('google-play-badge-en.png')
  })

  function badgeImage(): HTMLImageElement {
    const element: HTMLElement = fixture.nativeElement
    const image = element.querySelector<HTMLImageElement>('.play-logo')

    if (!image) {
      throw new Error('Expected the footer badge image to be rendered')
    }
    return image
  }
})
