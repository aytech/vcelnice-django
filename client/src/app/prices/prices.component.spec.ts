import { signal } from '@angular/core'
import { ComponentFixture, TestBed } from '@angular/core/testing'
import { NgbActiveModal, NgbModal } from '@ng-bootstrap/ng-bootstrap'
import { Subject } from 'rxjs'
import { Culture, Price } from '@interfaces'
import { LanguageService, PriceService } from '@services'
import { PricesComponent, ReservationModalComponent } from './prices.component'

describe('PricesComponent', () => {
  let fixture: ComponentFixture<PricesComponent>
  let priceResponse: Subject<Price[]>
  let priceService: jasmine.SpyObj<PriceService>
  let modalService: jasmine.SpyObj<NgbModal>
  let activeModal: jasmine.SpyObj<NgbActiveModal>

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
    const culturesSignal = signal(cultures)
    priceResponse = new Subject<Price[]>()
    priceService = jasmine.createSpyObj<PriceService>('PriceService', ['getPrices'])
    priceService.getPrices.and.returnValue(priceResponse)
    modalService = jasmine.createSpyObj<NgbModal>('NgbModal', ['open'])
    activeModal = jasmine.createSpyObj<NgbActiveModal>('NgbActiveModal', ['close', 'dismiss'])

    await TestBed.configureTestingModule({
      declarations: [PricesComponent, ReservationModalComponent],
      providers: [
        { provide: NgbActiveModal, useValue: activeModal },
        { provide: NgbModal, useValue: modalService },
        { provide: PriceService, useValue: priceService },
        {
          provide: LanguageService,
          useValue: {
            culturesSignal: culturesSignal.asReadonly()
          }
        }
      ]
    }).compileComponents()

    fixture = TestBed.createComponent(PricesComponent)
    fixture.autoDetectChanges()
  })

  it('replaces the loading indicator with API data when the resource resolves', async () => {
    const price: Price = {
      amount_description: 'Počet sklenic',
      id: 1,
      image: '/media/honey.jpg',
      in_store: 10,
      price: '250',
      title: 'Květový med',
      weight: '950 g'
    }

    expect(fixture.nativeElement.querySelector('.spinner')).not.toBeNull()

    priceResponse.next([price])
    priceResponse.complete()
    await fixture.whenStable()

    expect(fixture.nativeElement.querySelector('.spinner')).toBeNull()
    expect(fixture.nativeElement.textContent).toContain(price.title)
  })

  it('replaces the loading indicator with an error state when the resource fails', async () => {
    expect(fixture.nativeElement.querySelector('.spinner')).not.toBeNull()

    priceResponse.error(new Error('Request failed'))
    await fixture.whenStable()

    expect(fixture.nativeElement.querySelector('.spinner')).toBeNull()
    expect(fixture.nativeElement.querySelector('[role="alert"]')).not.toBeNull()
  })

  it('updates reservation modal state through signals', () => {
    const reservation = {
      title: signal(''),
      amountDescription: signal('')
    }
    modalService.open.and.returnValue({componentInstance: reservation} as any)

    fixture.componentInstance.openReservationForm({
      amount_description: '',
      id: 1,
      image: '/media/honey.jpg',
      in_store: 10,
      price: '250',
      title: 'Květový med',
      weight: '950 g'
    })

    expect(reservation.title()).toBe('Květový med')
    expect(reservation.amountDescription()).toBe('')
  })

  it('uses the Bootstrap 5 close button and preserves reservation dismissal', () => {
    const reservationFixture = TestBed.createComponent(ReservationModalComponent)
    reservationFixture.detectChanges()

    const closeButton = reservationFixture.nativeElement.querySelector(
      'button[aria-label="Close"]'
    ) as HTMLButtonElement | null

    expect(closeButton).not.toBeNull()
    expect(closeButton?.classList.contains('btn-close')).toBeTrue()
    expect(closeButton?.classList.contains('close')).toBeFalse()
    expect(closeButton?.querySelector('span')).toBeNull()

    closeButton?.click()

    expect(activeModal.dismiss).toHaveBeenCalledOnceWith('Cross click')
  })
})
