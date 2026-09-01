import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { RegionComponent } from './region.component';

describe('RegionComponent', () => {
  let component: RegionComponent;
  let fixture: ComponentFixture<RegionComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ RegionComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RegionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('keeps offset links within the Bootstrap grid width', () => {
    const links: HTMLElement[] = Array.from(
      fixture.nativeElement.querySelectorAll('.link')
    );

    expect(links.length).toBe(2);
    links.forEach(link => {
      expect(link.classList.contains('col-md-7')).toBeTrue();
      expect(link.classList.contains('offset-md-5')).toBeTrue();
      expect(link.classList.contains('col-lg-8')).toBeTrue();
      expect(link.classList.contains('offset-lg-4')).toBeTrue();
    });
  });
});
