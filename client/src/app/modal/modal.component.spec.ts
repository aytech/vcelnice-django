import { TemplateRef } from '@angular/core'
import { ComponentFixture, TestBed } from '@angular/core/testing'
import { NgbModal } from '@ng-bootstrap/ng-bootstrap'
import { ModalComponent } from './modal.component'

describe('ModalComponent', () => {
  let fixture: ComponentFixture<ModalComponent>
  let modalService: jasmine.SpyObj<NgbModal>

  beforeEach(async () => {
    modalService = jasmine.createSpyObj<NgbModal>('NgbModal', ['open'])
    modalService.open.and.returnValue({result: Promise.resolve()} as any)

    await TestBed.configureTestingModule({
      declarations: [ModalComponent],
      providers: [
        {provide: NgbModal, useValue: modalService}
      ]
    }).compileComponents()

    fixture = TestBed.createComponent(ModalComponent)
    fixture.detectChanges()
  })

  it('uses the Bootstrap 5 close button and preserves dismiss behavior', () => {
    const dismiss = jasmine.createSpy('dismiss')

    fixture.componentInstance.open('Title', 'Body')

    const template = modalService.open.calls.mostRecent().args[0] as TemplateRef<{
      close: () => void
      dismiss: (reason: string) => void
    }>
    const view = template.createEmbeddedView({close: jasmine.createSpy('close'), dismiss})
    view.detectChanges()

    const host = document.createElement('div')
    view.rootNodes.forEach(node => host.appendChild(node))
    const closeButton = host.querySelector<HTMLButtonElement>('button[aria-label="Close"]')

    expect(closeButton).not.toBeNull()
    expect(closeButton?.classList.contains('btn-close')).toBeTrue()
    expect(closeButton?.classList.contains('close')).toBeFalse()
    expect(closeButton?.querySelector('span')).toBeNull()

    closeButton?.click()

    expect(dismiss).toHaveBeenCalledOnceWith('Cross click')
    view.destroy()
  })
})
