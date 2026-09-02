import { HttpErrorResponse } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { catchError, map, of, switchMap } from 'rxjs';
import { KhorneService } from '../../../services/khorne/khorne.service';
import { loadKhorne, loadKhorneFailure, loadKhorneSuccess } from './khorne.action';

@Injectable()
export class KhorneEffects {
  private actions$ = inject(Actions);
  private service = inject(KhorneService);

  loadGuide$ = createEffect(() =>
    this.actions$.pipe(
      ofType(loadKhorne),
      switchMap(() =>
        this.service.getFaction().pipe(
          map((faction) => loadKhorneSuccess({ faction })),
          catchError((error: unknown) => {
            const message = error instanceof HttpErrorResponse
              ? `โหลดข้อมูลไม่สำเร็จ (${error.status})`
              : error instanceof Error
                ? error.message
                : 'โหลดข้อมูลไม่สำเร็จ';
            return of(loadKhorneFailure({ error: message }));
          })
        )
      )
    )
  );
}
