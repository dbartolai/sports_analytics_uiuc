export interface Dev {
  id: number;
  name: string;
  major: string;
  grad_year: number;
  fun_fact?: string;
}

export interface DevCreate {
  name: string;
  major: string;
  grad_year: number;
  fun_fact?: string;
}

export interface DevUpdate {
  name?: string;
  major?: string;
  grad_year?: number;
  fun_fact?: string;
}
