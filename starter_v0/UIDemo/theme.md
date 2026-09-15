---
version: beta-ios26
name: iOS-26-Liquid-Glass-Agent-Dashboard
description: A content-first agent chat dashboard inspired by iOS 26. A restrained Liquid Glass functional layer floats above a calm content layer; controls bend light, adapt to their background, morph between related states, and respond with spring-based motion. Tool traces remain readable and evidence-first.

colors:
  accent: "#007AFF"
  accent-pressed: "#0068D9"
  accent-on-dark: "#0A84FF"
  success: "#34C759"
  warning: "#FF9F0A"
  danger: "#FF3B30"
  info: "#5AC8FA"
  ink: "#1D1D1F"
  ink-secondary: "rgba(29, 29, 31, 0.68)"
  ink-tertiary: "rgba(29, 29, 31, 0.45)"
  ink-on-dark: "#FFFFFF"
  canvas: "#F5F5F7"
  content-surface: "#FFFFFF"
  content-surface-dark: "#1C1C1E"
  divider: "rgba(60, 60, 67, 0.16)"
  glass-highlight: "rgba(255, 255, 255, 0.72)"
  glass-border: "rgba(255, 255, 255, 0.46)"

materials:
  glass-regular:
    background: "rgba(246, 246, 248, 0.68)"
    backdropFilter: "saturate(180%) blur(22px)"
    border: "1px solid rgba(255, 255, 255, 0.46)"
    innerHighlight: "inset 0 1px 0 rgba(255, 255, 255, 0.58)"
    shadow: "0 8px 30px rgba(0, 0, 0, 0.12)"
  glass-clear:
    background: "rgba(255, 255, 255, 0.22)"
    backdropFilter: "saturate(190%) blur(14px)"
    border: "1px solid rgba(255, 255, 255, 0.38)"
    innerHighlight: "inset 0 1px 0 rgba(255, 255, 255, 0.52)"
    shadow: "0 10px 34px rgba(0, 0, 0, 0.14)"
  content-regular:
    background: "#FFFFFF"
    border: "1px solid rgba(60, 60, 67, 0.12)"
    shadow: "none"
  content-muted:
    background: "rgba(118, 118, 128, 0.08)"
    border: "1px solid rgba(60, 60, 67, 0.10)"
    shadow: "none"

typography:
  large-title: {fontFamily: "SF Pro Display, system-ui, -apple-system, BlinkMacSystemFont, sans-serif", fontSize: 34px, fontWeight: 700, lineHeight: 1.12, letterSpacing: -0.68px}
  title-1: {fontFamily: "SF Pro Display, system-ui, -apple-system, BlinkMacSystemFont, sans-serif", fontSize: 28px, fontWeight: 700, lineHeight: 1.18, letterSpacing: -0.42px}
  title-2: {fontFamily: "SF Pro Display, system-ui, -apple-system, BlinkMacSystemFont, sans-serif", fontSize: 22px, fontWeight: 600, lineHeight: 1.22, letterSpacing: -0.26px}
  headline: {fontFamily: "SF Pro Text, system-ui, -apple-system, BlinkMacSystemFont, sans-serif", fontSize: 17px, fontWeight: 600, lineHeight: 1.29, letterSpacing: -0.18px}
  body: {fontFamily: "SF Pro Text, system-ui, -apple-system, BlinkMacSystemFont, sans-serif", fontSize: 17px, fontWeight: 400, lineHeight: 1.47, letterSpacing: -0.18px}
  subheadline: {fontFamily: "SF Pro Text, system-ui, -apple-system, BlinkMacSystemFont, sans-serif", fontSize: 15px, fontWeight: 400, lineHeight: 1.4, letterSpacing: -0.08px}
  caption: {fontFamily: "SF Pro Text, system-ui, -apple-system, BlinkMacSystemFont, sans-serif", fontSize: 12px, fontWeight: 500, lineHeight: 1.33, letterSpacing: 0}
  mono: {fontFamily: "SFMono-Regular, ui-monospace, Cascadia Code, Consolas, monospace", fontSize: 13px, fontWeight: 400, lineHeight: 1.5, letterSpacing: 0}

rounded: {xs: 8px, sm: 12px, md: 16px, lg: 22px, xl: 28px, pill: 9999px, circle: 50%}
spacing: {xxs: 4px, xs: 8px, sm: 12px, md: 16px, lg: 24px, xl: 32px, xxl: 48px, section: 64px}

motion:
  duration-instant: 100ms
  duration-fast: 180ms
  duration-base: 280ms
  duration-slow: 420ms
  duration-present: 520ms
  ease-standard: "cubic-bezier(0.22, 1, 0.36, 1)"
  ease-exit: "cubic-bezier(0.4, 0, 1, 1)"
  spring-snappy: "linear(0, 0.42, 0.78, 1.04, 1.08, 1.03, 1)"
  spring-fluid: "linear(0, 0.19, 0.55, 0.86, 1.03, 1.06, 1.02, 1)"
  press-scale: 0.96
  hover-lift: -1px
  glass-shift-max: 3px

components:
  floating-navigation: {material: "{materials.glass-regular}", typography: "{typography.headline}", rounded: "{rounded.xl}", height: 56px, padding: 8px 12px}
  sidebar: {material: "{materials.glass-regular}", rounded: "{rounded.xl}", width: 300px, padding: 16px}
  composer: {material: "{materials.glass-regular}", rounded: "{rounded.xl}", minHeight: 56px, padding: 8px 10px 8px 18px}
  primary-button: {backgroundColor: "{colors.accent}", textColor: "#FFFFFF", typography: "{typography.headline}", rounded: "{rounded.pill}", minHeight: 44px, padding: 10px 18px}
  glass-button: {material: "{materials.glass-clear}", textColor: "{colors.ink}", rounded: "{rounded.pill}", minSize: 44px}
  chat-user: {backgroundColor: "{colors.accent}", textColor: "#FFFFFF", typography: "{typography.body}", rounded: "22px 22px 6px 22px", padding: 11px 15px}
  chat-agent: {material: "{materials.content-muted}", textColor: "{colors.ink}", typography: "{typography.body}", rounded: "22px 22px 22px 6px", padding: 12px 16px}
  tool-trace-card: {material: "{materials.content-regular}", rounded: "{rounded.lg}", padding: 16px}
  code-block: {backgroundColor: "rgba(118, 118, 128, 0.10)", textColor: "{colors.ink}", typography: "{typography.mono}", rounded: "{rounded.sm}", padding: 12px}
  sheet: {material: "{materials.glass-regular}", rounded: "{rounded.xl} {rounded.xl} 0 0", padding: 24px}
  toast: {material: "{materials.glass-regular}", rounded: "{rounded.pill}", padding: 10px 16px}
---

# iOS 26 Liquid Glass Theme — Agent Chat Dashboard

## 1. Design intent

Đây là cách diễn giải ngôn ngữ iOS 26 cho dashboard chat trên web, không phải bản sao màn hình iPhone. Giao diện phải có chiều sâu, phản hồi tự nhiên và chuyển động liền mạch, nhưng dữ liệu tool vẫn phải dễ đọc và kiểm chứng.

Giao diện gồm hai lớp rõ ràng:

1. **Content layer:** chat, tool trace, JSON, transcript, báo cáo và lỗi. Dùng nền đặc hoặc standard material để đọc ổn định.
2. **Functional Liquid Glass layer:** navigation, sidebar, composer, menu, popover, sheet và nút nổi. Lớp này nổi trên content và thích ứng với nội dung bên dưới.

Không biến mọi card thành kính. Liquid Glass chỉ dành cho điều hướng và điều khiển; nội dung mới là chủ thể.

## 2. Liquid Glass

- Dùng `glass-regular` cho navigation, sidebar, composer, popover và sheet có chữ.
- Chỉ dùng `glass-clear` cho control nhỏ trên nền giàu hình ảnh/màu sắc.
- Nếu nền quá sáng, thêm scrim đen tối đa 35% sau clear glass.
- Glass phải tự thích ứng light/dark và luôn giữ tương phản chữ/icon.
- Không lồng glass trong glass. Gom các control liên quan vào một glass container chung.
- Không dùng glass cho JSON dài, tool output, error detail hoặc nội dung transcript.
- Trình duyệt không hỗ trợ `backdrop-filter` phải fallback sang nền đặc `rgba(246,246,248,.96)`.

Web chỉ mô phỏng lensing bằng blur, saturation, viền highlight, inset highlight và shadow nhẹ. Không làm méo chữ/icon, không dùng chromatic aberration hoặc displacement filter nặng.

## 3. Bố cục UI Demo

### Floating navigation

Thanh trên nổi cách mép 12–16px, hiển thị tên app, trạng thái kết nối, provider/model, version, artifact hash, tải transcript và tạo session mới. Khi scroll có thể co từ 56px xuống 48px; nội dung crossfade và tái định vị trong cùng một hình kính.

### Sidebar / settings sheet

Desktop dùng một glass group duy nhất cho provider, model, version, history window, max tool rounds, theme và danh sách tool. Dưới 834px, sidebar morph thành bottom sheet từ nút Settings, có drag handle, nút đóng và hỗ trợ Escape.

Không hiển thị API key mặc định. Nếu cho phép nhập key cục bộ, dùng password field, không ghi vào log/transcript và xóa khỏi state khi kết thúc session.

### Conversation feed

Feed là content layer yên tĩnh, scroll bên dưới navigation và composer; scroll-edge blur bảo đảm control dễ đọc. User bubble màu xanh căn phải, agent bubble nền trung tính căn trái. Prose rộng tối đa 720px; trace tối đa 920px. Tin nhắn mới fade + dịch lên 10px trong 280ms; không animate lại lịch sử khi rerender.

### Tool trace timeline

Mỗi event bắt buộc hiện tool name, input JSON, output/error, round và status. Dòng thu gọn gồm icon, tên tool, tóm tắt args, badge và chevron. Khi mở rộng, chính card đó morph để lộ Input/Output; không mở modal rời.

- Queued: glyph trung tính.
- Running: một progress sweep hữu hạn và breathing opacity rất nhẹ.
- Succeeded: check xanh vẽ một lần rồi dừng.
- Waiting for user: icon cam, chuyển focus về composer.
- Failed: trạng thái đỏ và raw error an toàn phải nhìn thấy.

Không che tool thất bại hoặc thay raw evidence bằng summary trông như thành công.

### Composer

Composer là một capsule Liquid Glass nổi phía dưới, tôn trọng safe area. Input mở rộng mượt tối đa 6 dòng rồi scroll nội bộ. Send button phản hồi khi nhấn và morph thành activity indicator khi gửi. Clarification hiển thị ngay trên composer và tự focus input. Touch target tối thiểu 44×44px.

## 4. Motion system

Motion dùng để giải thích quan hệ và thay đổi trạng thái, không dùng để trang trí khi idle.

- Dùng spring cho thao tác trực tiếp, menu, sheet, disclosure và shared-element transition.
- Dùng opacity + translate nhẹ cho nội dung xuất hiện thụ động.
- Touch/pointer có phản hồi rõ hơn keyboard.
- Overshoot nhỏ; “liquid” nghĩa là liền mạch, không phải nảy quá mức.
- Không có chuyển động lắc/lơ lửng lặp vô hạn hoặc parallax liên tục.

| Interaction | Duration | Chuyển động |
|---|---:|---|
| Button press | 100–180ms | Scale 0.96, highlight hội tụ, spring về 1 |
| Glass hover | 180ms | Nhấc tối đa 1px, highlight dịch tối đa 3px |
| Expand trace | 280–420ms | Morph chiều cao/hình, rotate chevron, details fade trễ 60ms |
| Menu/popover | 280ms | Xuất phát từ trigger, scale 0.92→1, opacity 0→1 |
| Settings sheet | 420–520ms | Shared-origin morph + dim background |
| New message | 280ms | Opacity 0→1, translateY 10px→0 |
| Tool complete | 280ms | Progress morph thành status glyph, không nhảy layout |
| Toast | 280/180ms | Spring vào, ease ra |
| Version switch | 420ms | Indicator trượt, content crossfade |

Chỉ animate `transform` và `opacity` khi có thể. Không animate `backdrop-filter` liên tục. Giới hạn glass đang hoạt động đồng thời ở navigation, sidebar/sheet và composer.

## 5. State và micro-interaction

- Button: hover nhấc 1px; pressed scale 0.96; focus-visible có ring xanh 3px; disabled bỏ lens response.
- Segmented version: indicator trượt bằng spring, label đứng yên. Chỉ đổi nhãn version sau khi artifact thực sự được load.
- Tool disclosure: card morph liên tục, code fade sau khi expansion bắt đầu và giữ nguyên vị trí scroll.
- Confirmation: review sheet phải hiện chính xác summary, priority, asset ID và payload có thể thay đổi. Payload đổi thì confirmation cũ bị vô hiệu và phải hỏi lại.
- Error: màu đỏ chỉ dùng cho icon/label/leading indicator; nền card trung tính, raw safe error và recovery action vẫn hiển thị. Không rung toàn màn hình.

## 6. Accessibility

### Reduce Motion

Với `prefers-reduced-motion: reduce`, thay spring, scale, morph, parallax và pointer lensing bằng crossfade ≤150ms. Progress dùng chỉ báo tĩnh + text; focus và state announcement vẫn hoạt động.

### Reduce Transparency

Thay glass bằng surface đặc, bỏ blur/lensing nhưng giữ border, grouping và semantic status. Nên có tùy chọn fallback trong app khi browser không cung cấp preference này.

### Increase Contrast và truy cập chung

- Tăng opacity của glass và độ tương phản border.
- Mọi trạng thái màu phải kèm icon và text.
- Touch target tối thiểu 44×44px.
- Điều khiển hoàn toàn bằng keyboard, focus luôn nhìn thấy.
- Dùng `aria-live` thông báo thay đổi trạng thái tool nhưng không đọc toàn bộ JSON.
- Disclosure có `aria-expanded` và liên kết đúng panel.
- Hỗ trợ zoom 200% và reflow; code block được scroll nội bộ.

## 7. Responsive

| Breakpoint | Layout |
|---|---|
| ≥1440px | Content khóa 1440px, sidebar 300px, trace tối đa 920px |
| 1024–1439px | Sidebar 280px, conversation căn giữa |
| 834–1023px | Sidebar compact, tool summary ngắn hơn |
| 641–833px | Sidebar thành settings sheet, nav giản lược |
| ≤640px | Feed một cột, inset 12px, composer dùng toàn safe width |
| ≤419px | Large title còn 28px, metadata phụ chuyển vào details sheet |

Mobile composer phải đi theo bàn phím ảo và không che tin nhắn mới nhất.

## 8. Do / Don't

### Do

- Tách content dễ đọc khỏi functional glass nổi.
- Cho content scroll dưới navigation/composer với scroll-edge legibility effect.
- Gom control liên quan vào một glass container.
- Dùng morph và spring để giữ continuity giữa trigger và destination.
- Hiện rõ tool, args, result/error, version và transcript.
- Test trên nền sáng, tối, nhiều màu và nhiều chữ.
- Có fallback nền đặc và reduced motion.

### Don't

- Không áp glass lên mọi card, bubble và JSON block.
- Không nested glass.
- Không dùng blur thay cho hierarchy.
- Không dùng decorative gradient, animated blob, glow halo hay shimmer liên tục.
- Không bóp méo chữ/icon để giả refraction.
- Không bounce quá mức hoặc animation không mang ý nghĩa trạng thái.
- Không che lỗi hay confirmation payload vì mục đích thẩm mỹ.
- Không hiển thị, lưu hoặc đưa API key vào transcript.

## 9. Acceptance checklist

- [ ] Navigation hiện provider, model, version và artifact identity.
- [ ] Settings hiện cấu hình/tool mà không rò rỉ secret.
- [ ] Tool event hiện name, input JSON, output/error, round và state.
- [ ] Clarification focus composer và có waiting state rõ ràng.
- [ ] Ticket review đúng payload và invalidates stale confirmation.
- [ ] Nhiều tool trong một round hiển thị đúng thứ tự/quan hệ.
- [ ] Provider error vẫn nhìn thấy và có khả năng phục hồi.
- [ ] Transcript tự lưu và tải xuống JSON được.
- [ ] Glass chỉ dùng cho navigation/control.
- [ ] Press, expand, sheet, message, completion và version transitions đúng motion recipe.
- [ ] Reduced Motion, Reduced Transparency, keyboard, focus, contrast và zoom 200% đã kiểm tra.
- [ ] Mobile composer/settings sheet tôn trọng safe area và bàn phím.

## 10. Implementation note

Streamlit có thể mô phỏng visual bằng CSS injection, nhưng shared-element morph, pointer-aware lensing, interruptible spring và accessibility state đáng tin cậy sẽ dễ làm hơn bằng frontend tùy biến (Flask/FastAPI + HTML/CSS/JavaScript hoặc component framework). Dù chọn framework nào, agent loop Python và transcript schema hiện tại vẫn là source of truth.

## 11. Reference basis

Theme dựa trên Apple Human Interface Guidelines về Materials, Motion, Layout và các phiên WWDC25 về Liquid Glass. Đây là diễn giải cho dashboard web giáo dục, không tuyên bố tái tạo pixel-perfect private renderer của Apple.
