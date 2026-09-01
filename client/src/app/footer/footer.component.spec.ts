import { ComponentFixture, TestBed } from '@angular/core/testing'
import { RouterModule } from '@angular/router'
import { NgbModal } from '@ng-bootstrap/ng-bootstrap'
import { PrivacyComponent } from '../privacy/privacy.component'
import { FooterComponent } from './footer.component'

describe('FooterComponent', () => {
  let fixture: ComponentFixture<FooterComponent>
  let modalService: jasmine.SpyObj<NgbModal>

  beforeEach(async () => {
    modalService = jasmine.createSpyObj<NgbModal>('NgbModal', ['open'])

    await TestBed.configureTestingModule({
      declarations: [FooterComponent],
      imports: [RouterModule.forRoot([])],
      providers: [
        {provide: NgbModal, useValue: modalService}
      ]
    }).compileComponents()

    fixture = TestBed.createComponent(FooterComponent)
    fixture.detectChanges()
  })

  it('renders the footer navigation and attribution without a Google Play link', () => {
    const element: HTMLElement = fixture.nativeElement

    expect(element.querySelector('.footer-main')).not.toBeNull()
    expect(element.querySelector('.footer-bottom')).not.toBeNull()
    expect(element.querySelector('a[href*="play.google.com"]')).toBeNull()
    expect(element.querySelector('.play-logo')).toBeNull()
    expect(element.textContent).toContain('Jan Šaroch')
  })

  it('links Ceník and Kontakt to their landing-page sections', () => {
    const element: HTMLElement = fixture.nativeElement
    const links = Array.from(
      element.querySelectorAll<HTMLAnchorElement>('.footer-nav a')
    )
    const expectedLinks = new Map([
      ['Ceník', '#cenik'],
      ['Kontakt', '#kontakt']
    ])

    expectedLinks.forEach((fragment, label) => {
      const link = links.find(candidate => candidate.textContent?.trim() === label)

      expect(link).withContext(`${label} link`).toBeDefined()

      const url = new URL(link!.href)

      expect(url.pathname).withContext(`${label} path`).toBe('/')
      expect(url.hash).withContext(`${label} fragment`).toBe(fragment)
    })
  })

  it('opens privacy in a modal while preserving the direct URL', () => {
    const link = fixture.nativeElement.querySelector('.privacy-link') as HTMLAnchorElement
    const event = new MouseEvent('click', {bubbles: true, button: 0, cancelable: true})

    expect(new URL(link.href).pathname).toBe('/privacy')

    link.dispatchEvent(event)

    expect(event.defaultPrevented).toBeTrue()
    expect(modalService.open).toHaveBeenCalledTimes(1)

    const [content, options] = modalService.open.calls.mostRecent().args
    expect(content).toBe(PrivacyComponent)
    expect(options).toEqual(jasmine.objectContaining({
      ariaDescribedBy: 'privacy-modal-intro',
      ariaLabelledBy: 'privacy-modal-title',
      centered: true,
      fullscreen: 'sm',
      scrollable: true,
      size: 'lg'
    }))
  })

  it('leaves modified clicks available for opening the privacy route separately', () => {
    const event = new MouseEvent('click', {button: 0, cancelable: true, metaKey: true})

    fixture.componentInstance.openPrivacy(event)

    expect(event.defaultPrevented).toBeFalse()
    expect(modalService.open).not.toHaveBeenCalled()
  })
})
