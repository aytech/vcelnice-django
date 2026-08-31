import { NO_ERRORS_SCHEMA } from '@angular/core'
import { ComponentFixture, TestBed } from '@angular/core/testing'
import { Subject } from 'rxjs'
import { Article } from '@interfaces'
import { NewsService } from '@services'
import { NewsComponent } from './news.component'

describe('NewsComponent', () => {
  let fixture: ComponentFixture<NewsComponent>
  let newsResponse: Subject<Article[]>
  let newsService: jasmine.SpyObj<NewsService>

  beforeEach(async () => {
    newsResponse = new Subject<Article[]>()
    newsService = jasmine.createSpyObj<NewsService>('NewsService', ['getNews'])
    newsService.getNews.and.returnValue(newsResponse)

    await TestBed.configureTestingModule({
      declarations: [NewsComponent],
      providers: [{ provide: NewsService, useValue: newsService }],
      schemas: [NO_ERRORS_SCHEMA]
    }).compileComponents()

    fixture = TestBed.createComponent(NewsComponent)
    fixture.autoDetectChanges()
  })

  it('replaces the loading indicator with API data when the resource resolves', async () => {
    const article: Article = {
      id: 1,
      title: 'Medová sezóna',
      text: 'První letošní med je připraven.',
      icon: '',
      created: '2026-08-31',
      updated: '2026-08-31'
    }

    expect(fixture.nativeElement.querySelector('.spinner')).not.toBeNull()

    newsResponse.next([article])
    newsResponse.complete()
    await fixture.whenStable()

    expect(fixture.nativeElement.querySelector('.spinner')).toBeNull()
    expect(fixture.nativeElement.querySelector('.card-title')?.textContent).toContain(article.title)
  })

  it('replaces the loading indicator with an error state when the resource fails', async () => {
    expect(fixture.nativeElement.querySelector('.spinner')).not.toBeNull()

    newsResponse.error(new Error('Request failed'))
    await fixture.whenStable()

    expect(fixture.nativeElement.querySelector('.spinner')).toBeNull()
    expect(fixture.nativeElement.querySelector('[role="alert"]')).not.toBeNull()
  })
})
