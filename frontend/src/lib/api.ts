import axios from "axios";
import type {
  BgmResponse,
  ConversationResponse,
  ResultResponse,
  SynthesizeResponse,
  TaskStatus,
  UploadResponse,
} from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

const client = axios.create({
  baseURL: API_BASE,
  timeout: 120000,
});

export async function uploadVideo(
  file: File,
  era: string,
  creativeBrief: string,
  apiKey: string,
): Promise<UploadResponse> {
  const form = new FormData();
  form.append("file", file);
  form.append("era", era);
  form.append("creative_brief", creativeBrief);
  form.append("api_key", apiKey);
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

export async function getConversation(taskId: string): Promise<ConversationResponse> {
  const { data } = await client.get<ConversationResponse>(`/api/conversation/${taskId}`);
  return data;
}

export async function stepConversation(
  taskId: string,
  feedback: string,
  apiKey: string,
): Promise<ConversationResponse> {
  const { data } = await client.post<ConversationResponse>(`/api/conversation/${taskId}/step`, {
    feedback,
    api_key: apiKey,
  });
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
