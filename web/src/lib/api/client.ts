/* Minimal API client wrapper used by frontend components
   Provides named export `apiClient` with get/post/put/delete methods.
*/
type RequestOptions = {
  headers?: Record<string, string>;
  query?: Record<string, string | number | boolean | undefined>;
  body?: any;
};

const buildUrl = (path: string, query?: Record<string, any>) => {
  const base = process.env.NEXT_PUBLIC_API_URL || '';
  const url = new URL(path, base || window?.location?.origin);
  if (query) {
    Object.entries(query).forEach(([k, v]) => {
      if (v !== undefined && v !== null) url.searchParams.set(k, String(v));
    });
  }
  return url.toString();
};

// Accept either a RequestOptions object or a plain body as the 3rd parameter.
async function request(method: string, path: string, dataOrOpts: any = {}) {
  let opts: RequestOptions = {};
  // If caller passed an object that looks like RequestOptions (has headers or query), use it.
  if (dataOrOpts && (dataOrOpts.headers !== undefined || dataOrOpts.query !== undefined || dataOrOpts.body !== undefined)) {
    opts = dataOrOpts as RequestOptions;
  } else if (dataOrOpts !== undefined) {
    // Otherwise treat it as the request body
    opts = { body: dataOrOpts };
  }

  const url = buildUrl(path, opts.query);
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(opts.headers || {}),
  };

  const res = await fetch(url, {
    method,
    headers,
    body: opts.body ? JSON.stringify(opts.body) : undefined,
    credentials: 'include',
  });

  const text = await res.text();
  try {
    const json = text ? JSON.parse(text) : null;
    if (!res.ok) throw json || new Error(res.statusText);
    return json;
  } catch (e) {
    if (!res.ok) throw e;
    return text;
  }
}

// API client for FastAPI backend
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface ApiConfig {
  headers?: Record<string, string>;
  token?: string;
  params?: Record<string, any>;
}

export class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private getHeaders(config?: ApiConfig): Record<string, string> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    if (config?.token) {
      headers['Authorization'] = `Bearer ${config.token}`;
    }

    if (config?.headers) {
      Object.assign(headers, config.headers);
    }

    return headers;
  }

  private buildQuery(params?: Record<string, any>): string {
    if (!params) return '';
    const qs = new URLSearchParams();
    Object.keys(params).forEach((k) => {
      const val = params[k];
      if (val === undefined || val === null) return;
      if (Array.isArray(val)) {
        val.forEach((v) => qs.append(k, String(v)));
      } else if (typeof val === 'object') {
        qs.append(k, JSON.stringify(val));
      } else {
        qs.append(k, String(val));
      }
    });
    const s = qs.toString();
    return s ? `?${s}` : '';
  }

  async get<T>(endpoint: string, config?: ApiConfig): Promise<T> {
    const url = `${this.baseUrl}${endpoint}${this.buildQuery(config?.params)}`;
    const response = await fetch(url, {
      method: 'GET',
      headers: this.getHeaders(config),
    });

    if (!response.ok) throw new Error(`API Error: ${response.statusText}`);
    return response.json();
  }

  async post<T>(endpoint: string, data?: any, config?: ApiConfig): Promise<T> {
    const url = `${this.baseUrl}${endpoint}${this.buildQuery(config?.params)}`;
    const response = await fetch(url, {
      method: 'POST',
      headers: this.getHeaders(config),
      body: data ? JSON.stringify(data) : undefined,
    });

    if (!response.ok) throw new Error(`API Error: ${response.statusText}`);
    return response.json();
  }

  async put<T>(endpoint: string, data?: any, config?: ApiConfig): Promise<T> {
    const url = `${this.baseUrl}${endpoint}${this.buildQuery(config?.params)}`;
    const response = await fetch(url, {
      method: 'PUT',
      headers: this.getHeaders(config),
      body: data ? JSON.stringify(data) : undefined,
    });

    if (!response.ok) throw new Error(`API Error: ${response.statusText}`);
    return response.json();
  }

  async delete<T>(endpoint: string, config?: ApiConfig): Promise<T> {
    const url = `${this.baseUrl}${endpoint}${this.buildQuery(config?.params)}`;
    const response = await fetch(url, {
      method: 'DELETE',
      headers: this.getHeaders(config),
    });

    if (!response.ok) throw new Error(`API Error: ${response.statusText}`);
    return response.json();
  }
}

export const apiClient = new ApiClient();
