import { NO_ERRORS_SCHEMA } from '@angular/core'
import { ComponentFixture, TestBed } from '@angular/core/testing'
import { Subject } from 'rxjs'
import { Recipe } from '@interfaces'
import { RecipeService } from '@services'
import { RecipesComponent } from './recipes.component'

describe('RecipesComponent', () => {
  let fixture: ComponentFixture<RecipesComponent>
  let recipeResponse: Subject<Recipe[]>
  let recipeService: jasmine.SpyObj<RecipeService>

  beforeEach(async () => {
    recipeResponse = new Subject<Recipe[]>()
    recipeService = jasmine.createSpyObj<RecipeService>('RecipeService', ['getRecipes'])
    recipeService.getRecipes.and.returnValue(recipeResponse)

    await TestBed.configureTestingModule({
      declarations: [RecipesComponent],
      providers: [{ provide: RecipeService, useValue: recipeService }],
      schemas: [NO_ERRORS_SCHEMA]
    }).compileComponents()

    fixture = TestBed.createComponent(RecipesComponent)
    fixture.autoDetectChanges()
  })

  it('replaces the loading indicator with API data when the resource resolves', async () => {
    const recipe: Recipe = {
      id: 1,
      title: 'Medové perníčky',
      preview: 'Jednoduchý recept s medem.',
      text: 'Smíchejte všechny suroviny.',
      thumb: '/media/gingerbread.jpg'
    }

    expect(fixture.nativeElement.querySelector('.spinner')).not.toBeNull()

    recipeResponse.next([recipe])
    recipeResponse.complete()
    await fixture.whenStable()

    expect(fixture.nativeElement.querySelector('.spinner')).toBeNull()
    expect(fixture.nativeElement.querySelector('.card-title')?.textContent).toContain(recipe.title)
  })

  it('replaces the loading indicator with an error state when the resource fails', async () => {
    expect(fixture.nativeElement.querySelector('.spinner')).not.toBeNull()

    recipeResponse.error(new Error('Request failed'))
    await fixture.whenStable()

    expect(fixture.nativeElement.querySelector('.spinner')).toBeNull()
    expect(fixture.nativeElement.querySelector('[role="alert"]')).not.toBeNull()
  })
})
