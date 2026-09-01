import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing'

import { ContactComponent } from './contact.component'

describe('ContactComponent', () => {
  let component: ContactComponent
  let fixture: ComponentFixture<ContactComponent>

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ ContactComponent ]
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

  it('renders full-width contact details without a portrait', () => {
    const element: HTMLElement = fixture.nativeElement
    const details = element.querySelector<HTMLElement>('.contact-details')

    expect(element.querySelector('.portrait')).toBeNull()
    expect(element.querySelector('img')).toBeNull()
    expect(details?.classList.contains('col-12')).toBeTrue()
    expect(details?.classList.contains('col-md-7')).toBeFalse()
    expect(element.querySelector('a[href^="tel:"]')).not.toBeNull()
    expect(element.querySelector('a[href^="https://www.google.com/maps/"]')).not.toBeNull()
    expect(element.querySelector('a[href^="mailto:"]')).not.toBeNull()
  })
})
