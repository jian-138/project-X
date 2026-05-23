import axios from "axios";
import type {
  UploadResponse,
  TaskStatus,
  ResultResponse,
  BgmResponse,
  SynthesizeResponse,
} from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const client = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
});

export async function uploadVideo(file: File, era: string): Promise<UploadResponse> {
  const form = new FormData();
  form.append("file", file);
  form.append("era", era);
  const { data } = await client.post<UploadResponse>("/api/upload", form);
  return data;
}

export async function getTaskStatus(taskId: string): Promise<TaskStatus> {
  const { data } = await client.get<TaskStatus>(`/api/task/${taskId}`);
  return data;
}

export async function getResult(taskId: string): Promise<ResultResponse> {
  const { data } = await client.get<ResultResponse>(`/api/result/${taskId}`);
  return data;
}

export async function matchBgm(taskId: string, era: string): Promise<BgmResponse> {
  const { data } = await client.post<BgmResponse>(`/api/task/${taskId}/bgm`, { era });
  return data;
}

export async function synthesizeVideo(taskId: string): Promise<SynthesizeResponse> {
  const { data } = await client.post<SynthesizeResponse>(`/api/task/${taskId}/synthesize`);
  return data;
}
