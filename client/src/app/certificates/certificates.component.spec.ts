import { signal } from '@angular/core'
import { ComponentFixture, TestBed } from '@angular/core/testing'
import { Subject } from 'rxjs'
import { Certificate, Culture } from '@interfaces'
import { CertificateService, LanguageService } from '@services'
import { CertificatesComponent } from './certificates.component'

describe('CertificatesComponent', () => {
  let fixture: ComponentFixture<CertificatesComponent>
  let certificateResponse: Subject<Certificate[]>
  let certificateService: jasmine.SpyObj<CertificateService>

  const cultures: Culture = {
    amount_description: 'Počet sklenic',
    certificates: 'Certifikáty',
    close: 'Zavřít',
    contact: 'Kontakt',
    czk: 'Kč',
    home: 'Domů',
    loading: 'Načítám',
    news: 'Novinky',
    not_in_store: 'Není skladem',
    photo: 'Foto',
    price_list: 'Ceník',
    prices_not_found: 'Ceníky nenalezeny',
    recipes: 'Recepty',
    region: 'Region',
    reservation_text: 'Pro rezervaci nás kontaktujte.',
    reserve: 'Rezervovat',
    video: 'Video'
  }

  beforeEach(async () => {
    certificateResponse = new Subject<Certificate[]>()
    certificateService = jasmine.createSpyObj<CertificateService>('CertificateService', ['getCertificates'])
    certificateService.getCertificates.and.returnValue(certificateResponse)

    await TestBed.configureTestingModule({
      declarations: [CertificatesComponent],
      providers: [
        { provide: CertificateService, useValue: certificateService },
        { provide: LanguageService, useValue: { culturesSignal: signal(cultures).asReadonly() } }
      ]
    }).compileComponents()

    fixture = TestBed.createComponent(CertificatesComponent)
    fixture.autoDetectChanges()
  })

  it('replaces the loading indicator with API data when the resource resolves', async () => {
    const certificate: Certificate = {
      id: 1,
      file: '/media/certificate.pdf',
      description: 'Český med',
      type: 'pdf'
    }

    expect(fixture.nativeElement.querySelector('.spinner')).not.toBeNull()

    certificateResponse.next([certificate])
    certificateResponse.complete()
    await fixture.whenStable()

    expect(fixture.nativeElement.querySelector('.spinner')).toBeNull()
    expect(fixture.nativeElement.querySelector('.card-title')?.textContent).toContain(certificate.description)
  })

  it('replaces the loading indicator with an error state when the resource fails', async () => {
    expect(fixture.nativeElement.querySelector('.spinner')).not.toBeNull()

    certificateResponse.error(new Error('Request failed'))
    await fixture.whenStable()

    expect(fixture.nativeElement.querySelector('.spinner')).toBeNull()
    expect(fixture.nativeElement.querySelector('[role="alert"]')).not.toBeNull()
  })
})
