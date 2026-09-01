import { ComponentFixture, TestBed } from '@angular/core/testing'
import { FooterComponent } from './footer.component'

describe('FooterComponent', () => {
  let fixture: ComponentFixture<FooterComponent>

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [FooterComponent]
    }).compileComponents()

    fixture = TestBed.createComponent(FooterComponent)
    fixture.detectChanges()
  })

  it('renders attribution without a Google Play link', () => {
    const element: HTMLElement = fixture.nativeElement

    expect(element.querySelector('a[href*="play.google.com"]')).toBeNull()
    expect(element.querySelector('.play-logo')).toBeNull()
    expect(element.textContent).toContain('Jan Šaroch')
  })
})
