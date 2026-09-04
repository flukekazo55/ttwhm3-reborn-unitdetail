import { HttpErrorResponse } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { catchError, map, of, switchMap } from 'rxjs';
import { DwarfsService } from '../../../services/dwarfs/dwarfs.service';
import { loadDwarfs, loadDwarfsFailure, loadDwarfsSuccess } from './dwarfs.action';

@Injectable()
export class DwarfsEffects {
  private actions$ = inject(Actions);
  private service = inject(DwarfsService);

  loadGuide$ = createEffect(() =>
    this.actions$.pipe(
      ofType(loadDwarfs),
      switchMap(() =>
        this.service.getFaction().pipe(
          map((faction) => loadDwarfsSuccess({ faction })),
          catchError((error: unknown) => {
            const message = error instanceof HttpErrorResponse
              ? `โหลดข้อมูลไม่สำเร็จ (${error.status})`
              : error instanceof Error
                ? error.message
                : 'โหลดข้อมูลไม่สำเร็จ';
            return of(loadDwarfsFailure({ error: message }));
          })
        )
      )
    )
  );
}
