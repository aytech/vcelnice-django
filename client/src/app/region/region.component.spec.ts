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

  it('presents the region with readable hierarchy and scannable facts', () => {
    const element: HTMLElement = fixture.nativeElement;
    const paragraphs = element.querySelectorAll('.region-copy > p');
    const facts = Array.from(element.querySelectorAll<HTMLElement>('.region-fact'));
    const factText = facts.map(fact => fact.textContent).join(' ');

    expect(element.querySelector('.section-eyebrow')?.textContent).toContain('Včelnice');
    expect(element.querySelector('h2')?.textContent).toContain('Region');
    expect(element.querySelector('h3')?.textContent).toContain('Karlštejnsko');
    expect(paragraphs.length).toBeGreaterThanOrEqual(2);
    expect(element.querySelector('.region-copy br')).toBeNull();
    expect(facts.length).toBe(3);
    expect(factText).toContain('330 km²');
    expect(factText).toContain('40 000');
    expect(factText).toContain('1 milion');
  });

  it('uses descriptive imagery and safe external links', () => {
    const element: HTMLElement = fixture.nativeElement;
    const image = element.querySelector<HTMLImageElement>('.region-image-frame img');
    const links = Array.from(
      element.querySelectorAll<HTMLAnchorElement>('.region-links a')
    );

    expect(image?.alt).toContain('Hrad Karlštejn');
    expect(image?.width).toBe(200);
    expect(image?.height).toBe(200);
    expect(image?.loading).toBe('lazy');
    expect(links.length).toBe(2);
    links.forEach(link => {
      expect(link.target).toBe('_blank');
      expect(link.relList.contains('noopener')).toBeTrue();
      expect(link.relList.contains('noreferrer')).toBeTrue();
    });
  });
});
