import { ComponentFixture, TestBed } from '@angular/core/testing'
import { RouterModule } from '@angular/router'
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap'
import { PrivacyComponent } from './privacy.component'

describe('PrivacyComponent as a page', () => {
  let fixture: ComponentFixture<PrivacyComponent>

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [PrivacyComponent],
      imports: [RouterModule.forRoot([])]
    }).compileComponents()

    fixture = TestBed.createComponent(PrivacyComponent)
    fixture.detectChanges()
  })

  it('renders directly without a modal context', () => {
    const element: HTMLElement = fixture.nativeElement

    expect(fixture.componentInstance.isModal).toBeFalse()
    expect(element.querySelector('#privacy-page-title')?.textContent).toContain('Zásady ochrany soukromí')
    expect(element.querySelector('.btn-close')).toBeNull()
  })

  it('renders the privacy statement in Czech', () => {
    const text = fixture.nativeElement.textContent as string

    expect(text).toContain('Náš závazek k ochraně soukromí')
    expect(text).toContain('Jaké údaje shromažďujeme a proč')
    expect(text).toContain('Tento web nepoužívá soubory cookie.')
    expect(text).toContain('Odkazy na jiné webové stránky')
    expect(text).not.toContain('Website Privacy Statement')
  })

  it('links contact requests to the landing-page Kontakt section', () => {
    const link = fixture.nativeElement.querySelector('a[fragment="kontakt"]') as HTMLAnchorElement
    const url = new URL(link.href)

    expect(url.pathname).toBe('/')
    expect(url.hash).toBe('#kontakt')
  })
})

describe('PrivacyComponent as a modal', () => {
  let fixture: ComponentFixture<PrivacyComponent>
  let activeModal: jasmine.SpyObj<NgbActiveModal>

  beforeEach(async () => {
    activeModal = jasmine.createSpyObj<NgbActiveModal>('NgbActiveModal', ['close', 'dismiss'])

    await TestBed.configureTestingModule({
      declarations: [PrivacyComponent],
      imports: [RouterModule.forRoot([])],
      providers: [
        {provide: NgbActiveModal, useValue: activeModal}
      ]
    }).compileComponents()

    fixture = TestBed.createComponent(PrivacyComponent)
    fixture.detectChanges()
  })

  it('provides accessible Bootstrap 5 close controls', () => {
    const element: HTMLElement = fixture.nativeElement
    const headerClose = element.querySelector<HTMLButtonElement>(
      'button.btn-close[aria-label="Zavřít"]'
    )
    const footerClose = element.querySelector<HTMLButtonElement>('.privacy-close-button')

    expect(fixture.componentInstance.isModal).toBeTrue()
    expect(element.querySelector('#privacy-modal-title')).not.toBeNull()
    expect(element.querySelector('.close')).toBeNull()
    expect(headerClose).not.toBeNull()
    expect(headerClose?.querySelector('span')).toBeNull()

    headerClose?.click()
    footerClose?.click()

    expect(activeModal.dismiss).toHaveBeenCalledOnceWith('Cross click')
    expect(activeModal.close).toHaveBeenCalledOnceWith('Close click')
  })
})
