import { provideHttpClient } from '@angular/common/http'
import {
  HttpTestingController,
  provideHttpClientTesting
} from '@angular/common/http/testing'
import { TestBed } from '@angular/core/testing'
import { ApiConstants } from '@config'
import { Recipe } from '@interfaces'

import { RecipeService } from './recipe.service'

describe('RecipeService', () => {
  let service: RecipeService
  let httpTesting: HttpTestingController

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        RecipeService,
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    })

    service = TestBed.inject(RecipeService)
    httpTesting = TestBed.inject(HttpTestingController)
  })

  afterEach(() => httpTesting.verify())

  it('loads recipes from the API response', () => {
    const recipes: Recipe[] = [{
      id: 1,
      thumb: '/media/recipe-thumb.jpg',
      title: 'Gingerbread',
      preview: 'Honey gingerbread',
      text: 'Recipe instructions'
    }]
    let result: typeof recipes | undefined

    service.getRecipes().subscribe(value => result = value)

    const request = httpTesting.expectOne({
      method: 'GET',
      url: ApiConstants.GET_RECIPES
    })
    request.flush({ recipes })

    expect(result).toEqual(recipes)
  })
})
