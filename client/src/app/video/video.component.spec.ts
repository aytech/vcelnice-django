import { ComponentFixture, TestBed } from '@angular/core/testing'
import { By } from '@angular/platform-browser'
import { Subject } from 'rxjs'
import { Video } from '@interfaces'
import { VideoService } from '@services'
import { LightboxService } from '../shared/lightbox/lightbox.service'
import { VideoComponent } from './video.component'

describe('VideoComponent', () => {
  let fixture: ComponentFixture<VideoComponent>
  let videoResponse: Subject<Video[]>
  let videoService: jasmine.SpyObj<VideoService>
  let lightbox: jasmine.SpyObj<LightboxService>

  beforeEach(async () => {
    videoResponse = new Subject<Video[]>()
    videoService = jasmine.createSpyObj<VideoService>('VideoService', ['getVideos'])
    videoService.getVideos.and.returnValue(videoResponse)
    lightbox = jasmine.createSpyObj<LightboxService>('LightboxService', ['openVideo'])

    await TestBed.configureTestingModule({
      declarations: [VideoComponent],
      providers: [
        { provide: VideoService, useValue: videoService },
        { provide: LightboxService, useValue: lightbox }
      ]
    }).compileComponents()

    fixture = TestBed.createComponent(VideoComponent)
    fixture.autoDetectChanges()
  })

  it('renders accessible video cards after the resource resolves', async () => {
    const videos: Video[] = [
      {
        youtube_id: 'abc123',
        caption: 'Vytáčení medu',
        description: 'Odebírání medových rámků ze včel.',
        thumb: '/media/extraction.jpg'
      },
      {
        youtube_id: 'def456',
        caption: 'Včely na česně',
        description: null,
        thumb: null
      }
    ]

    expect(fixture.nativeElement.querySelector('.spinner')).not.toBeNull()

    videoResponse.next(videos)
    videoResponse.complete()
    await fixture.whenStable()

    const element = fixture.nativeElement as HTMLElement
    const cards = element.querySelectorAll<HTMLElement>('article.video-card')
    const links = element.querySelectorAll<HTMLAnchorElement>('.video-link')
    const thumbnail = element.querySelector<HTMLImageElement>('.video-thumbnail')

    expect(fixture.nativeElement.querySelector('.spinner')).toBeNull()
    expect(element.querySelector('.section-eyebrow')?.textContent).toContain('Včelnice')
    expect(element.querySelector('.section-heading h2')?.textContent).toContain('Video')
    expect(cards.length).toBe(2)
    expect(links.length).toBe(2)
    expect(links[0].getAttribute('href')).toBe('https://youtu.be/abc123')
    expect(links[0].target).toBe('_blank')
    expect(links[0].rel).toContain('noopener')
    expect(links[0].getAttribute('aria-label')).toContain(videos[0].caption)
    expect(thumbnail?.getAttribute('src')).toBe(videos[0].thumb)
    expect(thumbnail?.alt).toBe(videos[0].caption)
    expect(thumbnail?.loading).toBe('lazy')
    expect(thumbnail?.decoding).toBe('async')
    expect(element.querySelector('.video-description')?.textContent)
      .toContain(videos[0].description as string)
    expect(element.querySelector('.video-placeholder')).not.toBeNull()

    const event = new MouseEvent('click', { button: 0, cancelable: true })
    fixture.debugElement.queryAll(By.css('.video-link'))[1].triggerEventHandler('click', event)

    expect(lightbox.openVideo).toHaveBeenCalledOnceWith(event, videos[1])
  })

  it('uses a neutral status when no videos are available', async () => {
    videoResponse.next([])
    videoResponse.complete()
    await fixture.whenStable()

    const emptyState = fixture.nativeElement.querySelector('.video-empty') as HTMLElement

    expect(fixture.nativeElement.querySelector('.spinner')).toBeNull()
    expect(emptyState).not.toBeNull()
    expect(emptyState.getAttribute('role')).toBe('status')
    expect(fixture.nativeElement.querySelector('[role="alert"]')).toBeNull()
  })

  it('replaces the loading indicator with an error state when the resource fails', async () => {
    expect(fixture.nativeElement.querySelector('.spinner')).not.toBeNull()

    videoResponse.error(new Error('Request failed'))
    await fixture.whenStable()

    expect(fixture.nativeElement.querySelector('.spinner')).toBeNull()
    expect(fixture.nativeElement.querySelector('[role="alert"]')).not.toBeNull()
  })
})
