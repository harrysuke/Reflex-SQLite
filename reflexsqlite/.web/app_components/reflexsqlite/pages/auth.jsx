
import {ReflexEvent,applyEventActions,isNotNullOrUndefined,isTrue,mergeSlotProps} from "$/utils/state"
import {useStateContext} from "$/utils/context-registry"
import {jsx} from "@emotion/react"
import {Fragment,memo,useCallback,useEffect} from "react"
import DebounceInput from "react-debounce-input"
import {addEvents} from "$/utils/context"
import {Button as RadixThemesButton,TextField as RadixThemesTextField} from "@radix-ui/themes"








export const Bare_comp_bfae0278ca00a6d5a31996a43704d74e_9365ca20 = /*#__PURE__*/ (() => {
const Bare_comp_bfae0278ca00a6d5a31996a43704d74e_9365ca20 = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state.auth_error_rx_state_
    )
});
Bare_comp_bfae0278ca00a6d5a31996a43704d74e_9365ca20.displayName = "Bare";
return Bare_comp_bfae0278ca00a6d5a31996a43704d74e_9365ca20;
})();

export const Cond_comp_b78841e0b50ee47da223aa9ed94d5886_9365ca20 = /*#__PURE__*/ (() => {
const Cond_comp_b78841e0b50ee47da223aa9ed94d5886_9365ca20 = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state")
    return(
        (!((reflex___state____state__reflexsqlite___state___base____auth_state.auth_error_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_b78841e0b50ee47da223aa9ed94d5886_9365ca20.displayName = "Cond";
return Cond_comp_b78841e0b50ee47da223aa9ed94d5886_9365ca20;
})();

export const Debounceinput_debounceinput_47f74ea199555fd3fb3bd7441a145e23_9365ca20 = /*#__PURE__*/ (() => {
const Debounceinput_debounceinput_47f74ea199555fd3fb3bd7441a145e23_9365ca20 = memo(({children, ...rest}) => {
    const on_change_7a1864a38229f424c3c5aa00e4700b10 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.set_login_name", ({ ["value"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__reflexsqlite___state___base____auth_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state")
    return(
        jsx(DebounceInput,{...mergeSlotProps(rest, ({ css:({ ["width"] : "100%", ["background"] : "#FFFFFF", ["border"] : "1px solid #E5E8F1", ["borderRadius"] : "9px", ["padding"] : "10px 12px", ["fontSize"] : "13px", ["color"] : "#111827" }), debounceTimeout:300, element:RadixThemesTextField.Root, onChange:on_change_7a1864a38229f424c3c5aa00e4700b10, placeholder:"demo", type:"text", value:(isNotNullOrUndefined(reflex___state____state__reflexsqlite___state___base____auth_state.login_name_rx_state_) ? reflex___state____state__reflexsqlite___state___base____auth_state.login_name_rx_state_ : "") }), "inputRef")},)
    )
});
Debounceinput_debounceinput_47f74ea199555fd3fb3bd7441a145e23_9365ca20.displayName = "DebounceInput";
return Debounceinput_debounceinput_47f74ea199555fd3fb3bd7441a145e23_9365ca20;
})();

export const Debounceinput_debounceinput_30eb4c6c84314f63895336c159c0b09e_9365ca20 = /*#__PURE__*/ (() => {
const Debounceinput_debounceinput_30eb4c6c84314f63895336c159c0b09e_9365ca20 = memo(({children, ...rest}) => {
    const on_change_ddfe49fffbf76ac9c5e9f52e8082bdd7 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.set_login_password", ({ ["value"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__reflexsqlite___state___base____auth_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state")
    return(
        jsx(DebounceInput,{...mergeSlotProps(rest, ({ css:({ ["width"] : "100%", ["background"] : "#FFFFFF", ["border"] : "1px solid #E5E8F1", ["borderRadius"] : "9px", ["padding"] : "10px 12px", ["fontSize"] : "13px", ["color"] : "#111827" }), debounceTimeout:300, element:RadixThemesTextField.Root, onChange:on_change_ddfe49fffbf76ac9c5e9f52e8082bdd7, placeholder:"\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022", type:"password", value:(isNotNullOrUndefined(reflex___state____state__reflexsqlite___state___base____auth_state.login_password_rx_state_) ? reflex___state____state__reflexsqlite___state___base____auth_state.login_password_rx_state_ : "") }), "inputRef")},)
    )
});
Debounceinput_debounceinput_30eb4c6c84314f63895336c159c0b09e_9365ca20.displayName = "DebounceInput";
return Debounceinput_debounceinput_30eb4c6c84314f63895336c159c0b09e_9365ca20;
})();

export const Button_button_0afb9b19f81d9aa863bc6e06a7a79a74_9365ca20 = /*#__PURE__*/ (() => {
const Button_button_0afb9b19f81d9aa863bc6e06a7a79a74_9365ca20 = memo(({children, ...rest}) => {
    const on_click_83b7eb650c29897fcdb209085fc6849d = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.sign_in", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__reflexsqlite___state___base____auth_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state")
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#4F46E5", ["color"] : "white", ["borderRadius"] : "9px", ["padding"] : "9px 16px", ["fontSize"] : "13px", ["fontWeight"] : "600", ["cursor"] : "pointer", ["&:hover"] : ({ ["background"] : "#4338CA" }), ["width"] : "100%", ["marginTop"] : "4px" }), disabled:reflex___state____state__reflexsqlite___state___base____auth_state.auth_busy_rx_state_, onClick:on_click_83b7eb650c29897fcdb209085fc6849d }))},children)
    )
});
Button_button_0afb9b19f81d9aa863bc6e06a7a79a74_9365ca20.displayName = "Button";
return Button_button_0afb9b19f81d9aa863bc6e06a7a79a74_9365ca20;
})();

export const Debounceinput_debounceinput_ebb3530c336700ae3db231a66da16311_9365ca20 = /*#__PURE__*/ (() => {
const Debounceinput_debounceinput_ebb3530c336700ae3db231a66da16311_9365ca20 = memo(({children, ...rest}) => {
    const on_change_a6717eddf97ea8cab2d200e1eaf82436 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.set_reg_username", ({ ["value"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__reflexsqlite___state___base____auth_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state")
    return(
        jsx(DebounceInput,{...mergeSlotProps(rest, ({ css:({ ["width"] : "100%", ["background"] : "#FFFFFF", ["border"] : "1px solid #E5E8F1", ["borderRadius"] : "9px", ["padding"] : "10px 12px", ["fontSize"] : "13px", ["color"] : "#111827" }), debounceTimeout:300, element:RadixThemesTextField.Root, onChange:on_change_a6717eddf97ea8cab2d200e1eaf82436, placeholder:"analyst_01", type:"text", value:(isNotNullOrUndefined(reflex___state____state__reflexsqlite___state___base____auth_state.reg_username_rx_state_) ? reflex___state____state__reflexsqlite___state___base____auth_state.reg_username_rx_state_ : "") }), "inputRef")},)
    )
});
Debounceinput_debounceinput_ebb3530c336700ae3db231a66da16311_9365ca20.displayName = "DebounceInput";
return Debounceinput_debounceinput_ebb3530c336700ae3db231a66da16311_9365ca20;
})();

export const Debounceinput_debounceinput_8566d52612ab5738b48b7a7773739667_9365ca20 = /*#__PURE__*/ (() => {
const Debounceinput_debounceinput_8566d52612ab5738b48b7a7773739667_9365ca20 = memo(({children, ...rest}) => {
    const on_change_1aec4376821f4e228401892609c095b6 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.set_reg_full_name", ({ ["value"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__reflexsqlite___state___base____auth_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state")
    return(
        jsx(DebounceInput,{...mergeSlotProps(rest, ({ css:({ ["width"] : "100%", ["background"] : "#FFFFFF", ["border"] : "1px solid #E5E8F1", ["borderRadius"] : "9px", ["padding"] : "10px 12px", ["fontSize"] : "13px", ["color"] : "#111827" }), debounceTimeout:300, element:RadixThemesTextField.Root, onChange:on_change_1aec4376821f4e228401892609c095b6, placeholder:"Optional", type:"text", value:(isNotNullOrUndefined(reflex___state____state__reflexsqlite___state___base____auth_state.reg_full_name_rx_state_) ? reflex___state____state__reflexsqlite___state___base____auth_state.reg_full_name_rx_state_ : "") }), "inputRef")},)
    )
});
Debounceinput_debounceinput_8566d52612ab5738b48b7a7773739667_9365ca20.displayName = "DebounceInput";
return Debounceinput_debounceinput_8566d52612ab5738b48b7a7773739667_9365ca20;
})();

export const Debounceinput_debounceinput_21cdf6a509e0d55768ffabea46d6b090_9365ca20 = /*#__PURE__*/ (() => {
const Debounceinput_debounceinput_21cdf6a509e0d55768ffabea46d6b090_9365ca20 = memo(({children, ...rest}) => {
    const on_change_02858f08b69a5935d5f4f866010d8d62 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.set_reg_email", ({ ["value"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__reflexsqlite___state___base____auth_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state")
    return(
        jsx(DebounceInput,{...mergeSlotProps(rest, ({ css:({ ["width"] : "100%", ["background"] : "#FFFFFF", ["border"] : "1px solid #E5E8F1", ["borderRadius"] : "9px", ["padding"] : "10px 12px", ["fontSize"] : "13px", ["color"] : "#111827" }), debounceTimeout:300, element:RadixThemesTextField.Root, onChange:on_change_02858f08b69a5935d5f4f866010d8d62, placeholder:"you@example.com", type:"text", value:(isNotNullOrUndefined(reflex___state____state__reflexsqlite___state___base____auth_state.reg_email_rx_state_) ? reflex___state____state__reflexsqlite___state___base____auth_state.reg_email_rx_state_ : "") }), "inputRef")},)
    )
});
Debounceinput_debounceinput_21cdf6a509e0d55768ffabea46d6b090_9365ca20.displayName = "DebounceInput";
return Debounceinput_debounceinput_21cdf6a509e0d55768ffabea46d6b090_9365ca20;
})();

export const Debounceinput_debounceinput_e78fa43ff3167f6b7068d39e95d576d4_9365ca20 = /*#__PURE__*/ (() => {
const Debounceinput_debounceinput_e78fa43ff3167f6b7068d39e95d576d4_9365ca20 = memo(({children, ...rest}) => {
    const on_change_c20d5792ae1fbe72bc19e4e950b2e215 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.set_reg_password", ({ ["value"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__reflexsqlite___state___base____auth_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state")
    return(
        jsx(DebounceInput,{...mergeSlotProps(rest, ({ css:({ ["width"] : "100%", ["background"] : "#FFFFFF", ["border"] : "1px solid #E5E8F1", ["borderRadius"] : "9px", ["padding"] : "10px 12px", ["fontSize"] : "13px", ["color"] : "#111827" }), debounceTimeout:300, element:RadixThemesTextField.Root, onChange:on_change_c20d5792ae1fbe72bc19e4e950b2e215, placeholder:"At least 8 characters", type:"password", value:(isNotNullOrUndefined(reflex___state____state__reflexsqlite___state___base____auth_state.reg_password_rx_state_) ? reflex___state____state__reflexsqlite___state___base____auth_state.reg_password_rx_state_ : "") }), "inputRef")},)
    )
});
Debounceinput_debounceinput_e78fa43ff3167f6b7068d39e95d576d4_9365ca20.displayName = "DebounceInput";
return Debounceinput_debounceinput_e78fa43ff3167f6b7068d39e95d576d4_9365ca20;
})();

export const Debounceinput_debounceinput_e97ff28308cb5ffd5c91910c8fd26f28_9365ca20 = /*#__PURE__*/ (() => {
const Debounceinput_debounceinput_e97ff28308cb5ffd5c91910c8fd26f28_9365ca20 = memo(({children, ...rest}) => {
    const on_change_9e838595888e9f5608745b258bdcf296 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.set_reg_confirm", ({ ["value"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__reflexsqlite___state___base____auth_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state")
    return(
        jsx(DebounceInput,{...mergeSlotProps(rest, ({ css:({ ["width"] : "100%", ["background"] : "#FFFFFF", ["border"] : "1px solid #E5E8F1", ["borderRadius"] : "9px", ["padding"] : "10px 12px", ["fontSize"] : "13px", ["color"] : "#111827" }), debounceTimeout:300, element:RadixThemesTextField.Root, onChange:on_change_9e838595888e9f5608745b258bdcf296, placeholder:"Repeat password", type:"password", value:(isNotNullOrUndefined(reflex___state____state__reflexsqlite___state___base____auth_state.reg_confirm_rx_state_) ? reflex___state____state__reflexsqlite___state___base____auth_state.reg_confirm_rx_state_ : "") }), "inputRef")},)
    )
});
Debounceinput_debounceinput_e97ff28308cb5ffd5c91910c8fd26f28_9365ca20.displayName = "DebounceInput";
return Debounceinput_debounceinput_e97ff28308cb5ffd5c91910c8fd26f28_9365ca20;
})();

export const Button_button_59cb474e2b1cab2921af30e3d1a0f6dc_9365ca20 = /*#__PURE__*/ (() => {
const Button_button_59cb474e2b1cab2921af30e3d1a0f6dc_9365ca20 = memo(({children, ...rest}) => {
    const on_click_7fc719eb86046cde6f8bd93439b3d866 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.sign_up", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__reflexsqlite___state___base____auth_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state")
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#4F46E5", ["color"] : "white", ["borderRadius"] : "9px", ["padding"] : "9px 16px", ["fontSize"] : "13px", ["fontWeight"] : "600", ["cursor"] : "pointer", ["&:hover"] : ({ ["background"] : "#4338CA" }), ["width"] : "100%", ["marginTop"] : "4px" }), disabled:reflex___state____state__reflexsqlite___state___base____auth_state.auth_busy_rx_state_, onClick:on_click_7fc719eb86046cde6f8bd93439b3d866 }))},children)
    )
});
Button_button_59cb474e2b1cab2921af30e3d1a0f6dc_9365ca20.displayName = "Button";
return Button_button_59cb474e2b1cab2921af30e3d1a0f6dc_9365ca20;
})();
