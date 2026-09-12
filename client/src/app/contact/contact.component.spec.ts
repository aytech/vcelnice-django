import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing'
import { By } from '@angular/platform-browser'

import { ContactComponent } from './contact.component'
import { LightboxService } from '../shared/lightbox/lightbox.service'

describe('ContactComponent', () => {
  let component: ContactComponent
  let fixture: ComponentFixture<ContactComponent>
  let lightbox: jasmine.SpyObj<LightboxService>

  beforeEach(waitForAsync(() => {
    lightbox = jasmine.createSpyObj<LightboxService>('LightboxService', ['openMap'])

    TestBed.configureTestingModule({
      declarations: [ ContactComponent ],
      providers: [{ provide: LightboxService, useValue: lightbox }]
    })
    .compileComponents()
  }))

  beforeEach(() => {
    fixture = TestBed.createComponent(ContactComponent)
    component = fixture.componentInstance
    fixture.detectChanges()
  })

  it('should create', () => {
    expect(component).toBeTruthy()
  })

  it('renders contact cards without a portrait', () => {
    const element: HTMLElement = fixture.nativeElement
    const details = element.querySelector<HTMLElement>('.contact-grid')

    expect(element.querySelector('.portrait')).toBeNull()
    expect(element.querySelector('img')).toBeNull()
    expect(details?.querySelectorAll('.contact-card').length).toBe(3)
    expect(element.querySelector('a[href^="tel:"]')).not.toBeNull()
    expect(element.querySelector('a[href^="https://www.google.com/maps/"]')).not.toBeNull()
    expect(element.querySelector('a[href^="mailto:"]')).not.toBeNull()
  })

  it('opens the map through the lightbox while retaining the original link', () => {
    const mapLink = fixture.debugElement.query(By.css('a[href^="https://www.google.com/maps/"]'))
    const event = new MouseEvent('click', { button: 0, cancelable: true })

    expect(mapLink.nativeElement.getAttribute('href')).toBe(
      'https://www.google.com/maps/search/Riegrova+376,+252+19+Rudná/'
    )
    mapLink.triggerEventHandler('click', event)

    expect(lightbox.openMap).toHaveBeenCalledOnceWith(event)
  })
})
