import { ComponentFixture, TestBed } from '@angular/core/testing'
import { Subject } from 'rxjs'
import { Video } from '@interfaces'
import { VideoService } from '@services'
import { VideoComponent } from './video.component'

describe('VideoComponent', () => {
  let fixture: ComponentFixture<VideoComponent>
  let videoResponse: Subject<Video[]>
  let videoService: jasmine.SpyObj<VideoService>

  beforeEach(async () => {
    videoResponse = new Subject<Video[]>()
    videoService = jasmine.createSpyObj<VideoService>('VideoService', ['getVideos'])
    videoService.getVideos.and.returnValue(videoResponse)

    await TestBed.configureTestingModule({
      declarations: [VideoComponent],
      providers: [{ provide: VideoService, useValue: videoService }]
    }).compileComponents()

    fixture = TestBed.createComponent(VideoComponent)
    fixture.autoDetectChanges()
  })

  it('replaces the loading indicator with API data when the resource resolves', async () => {
    const video: Video = {
      id: 1,
      youtube_id: 'abc123',
      caption: 'Vytáčení medu',
      thumb: '/media/extraction.jpg'
    }

    expect(fixture.nativeElement.querySelector('.spinner')).not.toBeNull()

    videoResponse.next([video])
    videoResponse.complete()
    await fixture.whenStable()

    expect(fixture.nativeElement.querySelector('.spinner')).toBeNull()
    expect(fixture.nativeElement.querySelector('.card-title')?.textContent).toContain(video.caption)
  })

  it('replaces the loading indicator with an error state when the resource fails', async () => {
    expect(fixture.nativeElement.querySelector('.spinner')).not.toBeNull()

    videoResponse.error(new Error('Request failed'))
    await fixture.whenStable()

    expect(fixture.nativeElement.querySelector('.spinner')).toBeNull()
    expect(fixture.nativeElement.querySelector('[role="alert"]')).not.toBeNull()
  })
})
