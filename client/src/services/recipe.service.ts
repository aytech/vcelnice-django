import { Injectable } from '@angular/core'
import { HttpClient } from '@angular/common/http'
import { map, Observable } from 'rxjs'
import { ApiConstants } from '@config'
import { Recipe } from '@interfaces'

@Injectable()
export class RecipeService {

  constructor(
    private http: HttpClient
  ) {
  }

  getRecipes(): Observable<Array<Recipe>> {
    return this.http
      .get<{recipes: Recipe[]}>(ApiConstants.GET_RECIPES)
      .pipe(map(response => response.recipes))
  }
}
