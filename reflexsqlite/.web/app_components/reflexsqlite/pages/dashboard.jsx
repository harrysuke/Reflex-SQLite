
import {ReflexEvent,applyEventActions,isTrue,mergeSlotProps} from "$/utils/state"
import {Box as RadixThemesBox,Button as RadixThemesButton,Flex as RadixThemesFlex,Select as RadixThemesSelect,Switch as RadixThemesSwitch,Text as RadixThemesText} from "@radix-ui/themes"
import {ClientSide,addEvents} from "$/utils/context"
import {Fragment,memo,useCallback,useEffect} from "react"
import {jsx} from "@emotion/react"
import {useStateContext} from "$/utils/context-registry"
import {Area as RechartsArea,Bar as RechartsBar,CartesianGrid as RechartsCartesianGrid,Legend as RechartsLegend,Line as RechartsLine,ResponsiveContainer as RechartsResponsiveContainer,Tooltip as RechartsTooltip,XAxis as RechartsXAxis,YAxis as RechartsYAxis} from "recharts"

const RechartsAreaChart = ClientSide(() => import('recharts').then((mod) => mod.AreaChart), "RechartsAreaChart")
const RechartsBarChart = ClientSide(() => import('recharts').then((mod) => mod.BarChart), "RechartsBarChart")
const RechartsLineChart = ClientSide(() => import('recharts').then((mod) => mod.LineChart), "RechartsLineChart")






export const Button_button_ce1f76161399883ad9e25c58dccd4ffa_32c100df = /*#__PURE__*/ (() => {
const Button_button_ce1f76161399883ad9e25c58dccd4ffa_32c100df = memo(({children, ...rest}) => {
    const on_click_791672e8a7a06c8222ff645442dda0c6 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state.choose_library", ({ ["library_id"] : "numpy" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#FAFBFE", ["border"] : "1px solid transparent", ["borderRadius"] : "9px", ["padding"] : "7px 9px", ["cursor"] : "pointer", ["width"] : "100%", ["textAlign"] : "left", ["&:hover"] : ({ ["border"] : "1px solid #E5E8F1", ["background"] : "#FFFFFF" }) }), onClick:on_click_791672e8a7a06c8222ff645442dda0c6 }))},children)
    )
});
Button_button_ce1f76161399883ad9e25c58dccd4ffa_32c100df.displayName = "Button";
return Button_button_ce1f76161399883ad9e25c58dccd4ffa_32c100df;
})();

export const Button_button_697f0f56d01a5d0d08106dbadb644c46_32c100df = /*#__PURE__*/ (() => {
const Button_button_697f0f56d01a5d0d08106dbadb644c46_32c100df = memo(({children, ...rest}) => {
    const on_click_079f1253573c23e804ef9ab4ae493922 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state.choose_library", ({ ["library_id"] : "pandas" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#FAFBFE", ["border"] : "1px solid transparent", ["borderRadius"] : "9px", ["padding"] : "7px 9px", ["cursor"] : "pointer", ["width"] : "100%", ["textAlign"] : "left", ["&:hover"] : ({ ["border"] : "1px solid #E5E8F1", ["background"] : "#FFFFFF" }) }), onClick:on_click_079f1253573c23e804ef9ab4ae493922 }))},children)
    )
});
Button_button_697f0f56d01a5d0d08106dbadb644c46_32c100df.displayName = "Button";
return Button_button_697f0f56d01a5d0d08106dbadb644c46_32c100df;
})();

export const Button_button_00639f932bf836285537da1a1bbfc611_32c100df = /*#__PURE__*/ (() => {
const Button_button_00639f932bf836285537da1a1bbfc611_32c100df = memo(({children, ...rest}) => {
    const on_click_c975f32d876cddfbc88a72e061d1f56a = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state.choose_library", ({ ["library_id"] : "matplotlib" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#FAFBFE", ["border"] : "1px solid transparent", ["borderRadius"] : "9px", ["padding"] : "7px 9px", ["cursor"] : "pointer", ["width"] : "100%", ["textAlign"] : "left", ["&:hover"] : ({ ["border"] : "1px solid #E5E8F1", ["background"] : "#FFFFFF" }) }), onClick:on_click_c975f32d876cddfbc88a72e061d1f56a }))},children)
    )
});
Button_button_00639f932bf836285537da1a1bbfc611_32c100df.displayName = "Button";
return Button_button_00639f932bf836285537da1a1bbfc611_32c100df;
})();

export const Button_button_f86790f043dda989e0c27dd9b2a3c36e_32c100df = /*#__PURE__*/ (() => {
const Button_button_f86790f043dda989e0c27dd9b2a3c36e_32c100df = memo(({children, ...rest}) => {
    const on_click_e1400e4bd8c31922695cde246e18785a = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state.choose_library", ({ ["library_id"] : "seaborn" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#FAFBFE", ["border"] : "1px solid transparent", ["borderRadius"] : "9px", ["padding"] : "7px 9px", ["cursor"] : "pointer", ["width"] : "100%", ["textAlign"] : "left", ["&:hover"] : ({ ["border"] : "1px solid #E5E8F1", ["background"] : "#FFFFFF" }) }), onClick:on_click_e1400e4bd8c31922695cde246e18785a }))},children)
    )
});
Button_button_f86790f043dda989e0c27dd9b2a3c36e_32c100df.displayName = "Button";
return Button_button_f86790f043dda989e0c27dd9b2a3c36e_32c100df;
})();

export const Button_button_e7cfea85af571847d94dc5aa9dedf40f_32c100df = /*#__PURE__*/ (() => {
const Button_button_e7cfea85af571847d94dc5aa9dedf40f_32c100df = memo(({children, ...rest}) => {
    const on_click_3a7dd40b050d0835ffd6b7fe99f3fc12 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state.choose_library", ({ ["library_id"] : "sklearn" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#FAFBFE", ["border"] : "1px solid transparent", ["borderRadius"] : "9px", ["padding"] : "7px 9px", ["cursor"] : "pointer", ["width"] : "100%", ["textAlign"] : "left", ["&:hover"] : ({ ["border"] : "1px solid #E5E8F1", ["background"] : "#FFFFFF" }) }), onClick:on_click_3a7dd40b050d0835ffd6b7fe99f3fc12 }))},children)
    )
});
Button_button_e7cfea85af571847d94dc5aa9dedf40f_32c100df.displayName = "Button";
return Button_button_e7cfea85af571847d94dc5aa9dedf40f_32c100df;
})();

export const Button_button_b5575478594af6ab2cd906a710cdfbe4_32c100df = /*#__PURE__*/ (() => {
const Button_button_b5575478594af6ab2cd906a710cdfbe4_32c100df = memo(({children, ...rest}) => {
    const on_click_818f1c5c61d84492101c741bb804ca3a = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state.choose_library", ({ ["library_id"] : "torch" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#FFFFFF", ["border"] : "1px solid transparent", ["borderRadius"] : "9px", ["padding"] : "7px 9px", ["cursor"] : "pointer", ["width"] : "100%", ["textAlign"] : "left", ["&:hover"] : ({ ["border"] : "1px solid #E5E8F1", ["background"] : "#FFFFFF" }) }), onClick:on_click_818f1c5c61d84492101c741bb804ca3a }))},children)
    )
});
Button_button_b5575478594af6ab2cd906a710cdfbe4_32c100df.displayName = "Button";
return Button_button_b5575478594af6ab2cd906a710cdfbe4_32c100df;
})();

export const Button_button_a69ae905019e323c127ca23066d87e7c_32c100df = /*#__PURE__*/ (() => {
const Button_button_a69ae905019e323c127ca23066d87e7c_32c100df = memo(({children, ...rest}) => {
    const on_click_5bec0f8897a5068ce9a32a24a1035a2b = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___explore_state____explore_state.choose_library", ({ ["library_id"] : "tensorflow" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#FFFFFF", ["border"] : "1px solid transparent", ["borderRadius"] : "9px", ["padding"] : "7px 9px", ["cursor"] : "pointer", ["width"] : "100%", ["textAlign"] : "left", ["&:hover"] : ({ ["border"] : "1px solid #E5E8F1", ["background"] : "#FFFFFF" }) }), onClick:on_click_5bec0f8897a5068ce9a32a24a1035a2b }))},children)
    )
});
Button_button_a69ae905019e323c127ca23066d87e7c_32c100df.displayName = "Button";
return Button_button_a69ae905019e323c127ca23066d87e7c_32c100df;
})();

export const Bare_comp_5ab6f538659d533714715a63cb92d666_32c100df = /*#__PURE__*/ (() => {
const Bare_comp_5ab6f538659d533714715a63cb92d666_32c100df = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state.initials_rx_state_
    )
});
Bare_comp_5ab6f538659d533714715a63cb92d666_32c100df.displayName = "Bare";
return Bare_comp_5ab6f538659d533714715a63cb92d666_32c100df;
})();

export const Box_box_c22865b79f321cbc36a1b8dbd5f84564_32c100df = /*#__PURE__*/ (() => {
const Box_box_c22865b79f321cbc36a1b8dbd5f84564_32c100df = memo(({children, ...rest}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state")
    return(
        jsx(RadixThemesBox,{...mergeSlotProps(rest, ({ css:({ ["background"] : reflex___state____state__reflexsqlite___state___base____auth_state.avatar_color_rx_state_, ["borderRadius"] : "999px", ["width"] : "32px", ["height"] : "32px", ["minWidth"] : "32px", ["display"] : "flex", ["alignItems"] : "center", ["justifyContent"] : "center" }) }))},children)
    )
});
Box_box_c22865b79f321cbc36a1b8dbd5f84564_32c100df.displayName = "Box";
return Box_box_c22865b79f321cbc36a1b8dbd5f84564_32c100df;
})();

export const Bare_comp_fbe62c4eb19f3c695844dc0427695e5a_32c100df = /*#__PURE__*/ (() => {
const Bare_comp_fbe62c4eb19f3c695844dc0427695e5a_32c100df = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state.display_name_rx_state_
    )
});
Bare_comp_fbe62c4eb19f3c695844dc0427695e5a_32c100df.displayName = "Bare";
return Bare_comp_fbe62c4eb19f3c695844dc0427695e5a_32c100df;
})();

export const Bare_comp_bcff288a0ef24fc2c402098247cbd23b_32c100df = /*#__PURE__*/ (() => {
const Bare_comp_bcff288a0ef24fc2c402098247cbd23b_32c100df = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state.role_rx_state_
    )
});
Bare_comp_bcff288a0ef24fc2c402098247cbd23b_32c100df.displayName = "Bare";
return Bare_comp_bcff288a0ef24fc2c402098247cbd23b_32c100df;
})();

export const Button_button_f9de5aac8983a4287e20b52d3112c0ce_32c100df = /*#__PURE__*/ (() => {
const Button_button_f9de5aac8983a4287e20b52d3112c0ce_32c100df = memo(({children, ...rest}) => {
    const on_click_42b68d07de6d2f872f818321f5b24e9f = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.sign_out", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#FFFFFF", ["color"] : "#111827", ["border"] : "1px solid #E5E8F1", ["borderRadius"] : "9px", ["padding"] : "9px 14px", ["fontSize"] : "13px", ["fontWeight"] : "500", ["cursor"] : "pointer", ["&:hover"] : ({ ["background"] : "#FAFBFE" }) }), onClick:on_click_42b68d07de6d2f872f818321f5b24e9f }))},children)
    )
});
Button_button_f9de5aac8983a4287e20b52d3112c0ce_32c100df.displayName = "Button";
return Button_button_f9de5aac8983a4287e20b52d3112c0ce_32c100df;
})();

export const Bare_comp_b77440ce799e2716fc94f715a4722763_32c100df = /*#__PURE__*/ (() => {
const Bare_comp_b77440ce799e2716fc94f715a4722763_32c100df = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state.dashboard_error_rx_state_
    )
});
Bare_comp_b77440ce799e2716fc94f715a4722763_32c100df.displayName = "Bare";
return Bare_comp_b77440ce799e2716fc94f715a4722763_32c100df;
})();

export const Cond_comp_ec3bb4d29f8cc2f817afeabef41f14c4_32c100df = /*#__PURE__*/ (() => {
const Cond_comp_ec3bb4d29f8cc2f817afeabef41f14c4_32c100df = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state")
    return(
        (!((reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state.dashboard_error_rx_state_?.valueOf?.() === ""?.valueOf?.()))?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_ec3bb4d29f8cc2f817afeabef41f14c4_32c100df.displayName = "Cond";
return Cond_comp_ec3bb4d29f8cc2f817afeabef41f14c4_32c100df;
})();

export const Foreach_comp_e043e0d8e711ee1ab59397397e64d6cf_32c100df = /*#__PURE__*/ (() => {
const Foreach_comp_e043e0d8e711ee1ab59397397e64d6cf_32c100df = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state")
    return(
        Array.prototype.map.call(reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state.datasets_rx_state_ ?? [],((item_rx_state_,index_05be63f1d173381cb3cb2f7405119c7a)=>(jsx(RadixThemesButton,{css:({ ["background"] : "#FAFBFE", ["border"] : "1px solid #E5E8F1", ["borderRadius"] : "9px", ["padding"] : "8px 12px", ["cursor"] : "pointer", ["&:hover"] : ({ ["border"] : "1px solid #C7D2FE" }) }),key:index_05be63f1d173381cb3cb2f7405119c7a,onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state.select_dataset", ({ ["dataset_id"] : item_rx_state_?.["id"] }), ({  })))], [_e], ({  }))))},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["gap"] : "8px", ["alignItems"] : "center" }),direction:"row",gap:"3"},jsx(RadixThemesBox,{css:({ ["width"] : "6px", ["height"] : "6px", ["minWidth"] : "6px", ["borderRadius"] : "999px", ["background"] : "#4F46E5" })},),jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["gap"] : "1px", ["alignItems"] : "start" }),direction:"column",gap:"3"},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "11px", ["fontWeight"] : "650", ["color"] : "#111827" })},item_rx_state_?.["name"]),jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "9px", ["color"] : "#64748B" })},(item_rx_state_?.["rows"]+" rows \u00b7 "+item_rx_state_?.["columns"]+" cols"))))))))
    )
});
Foreach_comp_e043e0d8e711ee1ab59397397e64d6cf_32c100df.displayName = "Foreach";
return Foreach_comp_e043e0d8e711ee1ab59397397e64d6cf_32c100df;
})();

export const Selectroot_select__root_d117030294ea698df88f11cfc6e6bd89_32c100df = /*#__PURE__*/ (() => {
const Selectroot_select__root_d117030294ea698df88f11cfc6e6bd89_32c100df = memo(({children, ...rest}) => {
    const on_change_64a51fcb24551bbd8cbdf7b36624f1d3 = useCallback(((_ev_0) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state.set_chart_type", ({ ["value"] : _ev_0 }), ({  })))], [_ev_0], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state")
    return(
        jsx(RadixThemesSelect.Root,{...mergeSlotProps(rest, ({ onValueChange:on_change_64a51fcb24551bbd8cbdf7b36624f1d3, size:"1", value:reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state.chart_type_rx_state_ }))},children)
    )
});
Selectroot_select__root_d117030294ea698df88f11cfc6e6bd89_32c100df.displayName = "SelectRoot";
return Selectroot_select__root_d117030294ea698df88f11cfc6e6bd89_32c100df;
})();

export const Foreach_comp_e509a6ec9fc191519bf3176d313ffbfd_32c100df = /*#__PURE__*/ (() => {
const Foreach_comp_e509a6ec9fc191519bf3176d313ffbfd_32c100df = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state")
    return(
        Array.prototype.map.call(reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state.x_options_rx_state_ ?? [],((item_rx_state_,index_a4c056de887ac0859af139cad1744de9)=>(jsx(RadixThemesSelect.Item,{key:index_a4c056de887ac0859af139cad1744de9,value:item_rx_state_},item_rx_state_))))
    )
});
Foreach_comp_e509a6ec9fc191519bf3176d313ffbfd_32c100df.displayName = "Foreach";
return Foreach_comp_e509a6ec9fc191519bf3176d313ffbfd_32c100df;
})();

export const Selectroot_select__root_8668e25ae585e454a13eb247732549b6_32c100df = /*#__PURE__*/ (() => {
const Selectroot_select__root_8668e25ae585e454a13eb247732549b6_32c100df = memo(({children, ...rest}) => {
    const on_change_aa812da70e21937953efaabdc1fdb9a6 = useCallback(((_ev_0) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state.set_x_column", ({ ["value"] : _ev_0 }), ({  })))], [_ev_0], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state")
    return(
        jsx(RadixThemesSelect.Root,{...mergeSlotProps(rest, ({ onValueChange:on_change_aa812da70e21937953efaabdc1fdb9a6, size:"1", value:reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state.x_column_rx_state_ }))},children)
    )
});
Selectroot_select__root_8668e25ae585e454a13eb247732549b6_32c100df.displayName = "SelectRoot";
return Selectroot_select__root_8668e25ae585e454a13eb247732549b6_32c100df;
})();

export const Foreach_comp_6789c4573a0526345708de81b455c32e_32c100df = /*#__PURE__*/ (() => {
const Foreach_comp_6789c4573a0526345708de81b455c32e_32c100df = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state")
    return(
        Array.prototype.map.call(reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state.y_options_rx_state_ ?? [],((item_rx_state_,index_a4c056de887ac0859af139cad1744de9)=>(jsx(RadixThemesSelect.Item,{key:index_a4c056de887ac0859af139cad1744de9,value:item_rx_state_},item_rx_state_))))
    )
});
Foreach_comp_6789c4573a0526345708de81b455c32e_32c100df.displayName = "Foreach";
return Foreach_comp_6789c4573a0526345708de81b455c32e_32c100df;
})();

export const Selectroot_select__root_61014c735b6684edbf015ee6c68b225b_32c100df = /*#__PURE__*/ (() => {
const Selectroot_select__root_61014c735b6684edbf015ee6c68b225b_32c100df = memo(({children, ...rest}) => {
    const on_change_55650bf5f8ca3b08a6785666ff5d3e68 = useCallback(((_ev_0) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state.set_y_column", ({ ["value"] : _ev_0 }), ({  })))], [_ev_0], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state")
    return(
        jsx(RadixThemesSelect.Root,{...mergeSlotProps(rest, ({ onValueChange:on_change_55650bf5f8ca3b08a6785666ff5d3e68, size:"1", value:reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state.y_column_rx_state_ }))},children)
    )
});
Selectroot_select__root_61014c735b6684edbf015ee6c68b225b_32c100df.displayName = "SelectRoot";
return Selectroot_select__root_61014c735b6684edbf015ee6c68b225b_32c100df;
})();

export const Switch_switch_346525e508726626da06ad8c2dba8550_32c100df = /*#__PURE__*/ (() => {
const Switch_switch_346525e508726626da06ad8c2dba8550_32c100df = memo(({children, ...rest}) => {
    const on_change_40354811b298cbe7c7e2d84dd86515fd = useCallback(((_ev_0) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state.toggle_live", ({ ["value"] : _ev_0 }), ({  })))], [_ev_0], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state")
    return(
        jsx(RadixThemesSwitch,{...mergeSlotProps(rest, ({ checked:reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state.live_enabled_rx_state_, onCheckedChange:on_change_40354811b298cbe7c7e2d84dd86515fd }))},)
    )
});
Switch_switch_346525e508726626da06ad8c2dba8550_32c100df.displayName = "Switch";
return Switch_switch_346525e508726626da06ad8c2dba8550_32c100df;
})();

export const Bare_comp_0f9f37acac1675d5c212d52b2601be10_32c100df = /*#__PURE__*/ (() => {
const Bare_comp_0f9f37acac1675d5c212d52b2601be10_32c100df = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state.tick_rx_state_
    )
});
Bare_comp_0f9f37acac1675d5c212d52b2601be10_32c100df.displayName = "Bare";
return Bare_comp_0f9f37acac1675d5c212d52b2601be10_32c100df;
})();

export const Button_button_136da1536ce8f515c67b2c71d3f6520a_32c100df = /*#__PURE__*/ (() => {
const Button_button_136da1536ce8f515c67b2c71d3f6520a_32c100df = memo(({children, ...rest}) => {
    const on_click_66bc1bfd465eb6f6caba72105a7338e5 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state.refresh_dashboard", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ css:({ ["background"] : "#FFFFFF", ["color"] : "#111827", ["border"] : "1px solid #E5E8F1", ["borderRadius"] : "9px", ["padding"] : "9px 14px", ["fontSize"] : "13px", ["fontWeight"] : "500", ["cursor"] : "pointer", ["&:hover"] : ({ ["background"] : "#FAFBFE" }) }), onClick:on_click_66bc1bfd465eb6f6caba72105a7338e5 }))},children)
    )
});
Button_button_136da1536ce8f515c67b2c71d3f6520a_32c100df.displayName = "Button";
return Button_button_136da1536ce8f515c67b2c71d3f6520a_32c100df;
})();

export const Bare_comp_3f190b1fb5ed4b1724c4a86eea43c71f_32c100df = /*#__PURE__*/ (() => {
const Bare_comp_3f190b1fb5ed4b1724c4a86eea43c71f_32c100df = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state.kpi_datasets_rx_state_
    )
});
Bare_comp_3f190b1fb5ed4b1724c4a86eea43c71f_32c100df.displayName = "Bare";
return Bare_comp_3f190b1fb5ed4b1724c4a86eea43c71f_32c100df;
})();

export const Bare_comp_b757511c9d5c72d6eb353f84454a3e41_32c100df = /*#__PURE__*/ (() => {
const Bare_comp_b757511c9d5c72d6eb353f84454a3e41_32c100df = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state.kpi_rows_rx_state_
    )
});
Bare_comp_b757511c9d5c72d6eb353f84454a3e41_32c100df.displayName = "Bare";
return Bare_comp_b757511c9d5c72d6eb353f84454a3e41_32c100df;
})();

export const Bare_comp_9d1d758b69dcdea0b673ee570bf21211_32c100df = /*#__PURE__*/ (() => {
const Bare_comp_9d1d758b69dcdea0b673ee570bf21211_32c100df = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state.kpi_columns_rx_state_
    )
});
Bare_comp_9d1d758b69dcdea0b673ee570bf21211_32c100df.displayName = "Bare";
return Bare_comp_9d1d758b69dcdea0b673ee570bf21211_32c100df;
})();

export const Bare_comp_3c3a7203f1084464b4cc3f547fcf1cae_32c100df = /*#__PURE__*/ (() => {
const Bare_comp_3c3a7203f1084464b4cc3f547fcf1cae_32c100df = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state.kpi_completeness_rx_state_
    )
});
Bare_comp_3c3a7203f1084464b4cc3f547fcf1cae_32c100df.displayName = "Bare";
return Bare_comp_3c3a7203f1084464b4cc3f547fcf1cae_32c100df;
})();

export const Bare_comp_4f8a19e18a783d95947d47e1d2ba0aeb_32c100df = /*#__PURE__*/ (() => {
const Bare_comp_4f8a19e18a783d95947d47e1d2ba0aeb_32c100df = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state.missing_hint_rx_state_
    )
});
Bare_comp_4f8a19e18a783d95947d47e1d2ba0aeb_32c100df.displayName = "Bare";
return Bare_comp_4f8a19e18a783d95947d47e1d2ba0aeb_32c100df;
})();

export const Bare_comp_5c9db9b2312eb2cb69e161fa28d4ed21_32c100df = /*#__PURE__*/ (() => {
const Bare_comp_5c9db9b2312eb2cb69e161fa28d4ed21_32c100df = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state")
    return(
        reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state.chart_subtitle_rx_state_
    )
});
Bare_comp_5c9db9b2312eb2cb69e161fa28d4ed21_32c100df.displayName = "Bare";
return Bare_comp_5c9db9b2312eb2cb69e161fa28d4ed21_32c100df;
})();

export const Responsivecontainer_responsivecontainer_7affce89a88ddfc4ad2f90798ff58e0b_32c100df = /*#__PURE__*/ (() => {
const Responsivecontainer_responsivecontainer_7affce89a88ddfc4ad2f90798ff58e0b_32c100df = memo(({children, ...rest}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state")
    return(
        jsx(RechartsResponsiveContainer,{...mergeSlotProps(rest, ({ height:300, minHeight:10, minWidth:10, width:"100%" }))},jsx(RechartsAreaChart,{data:reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state.chart_data_rx_state_,height:"100%",margin:({ ["top"] : 10, ["right"] : 16, ["left"] : 4, ["bottom"] : 6 }),width:"100%"},jsx(RechartsCartesianGrid,{stroke:"#EEF1F7",strokeDasharray:"3 3",vertical:false},),jsx(RechartsXAxis,{axisLine:false,dataKey:"name",height:28,stroke:"var(--gray-9)",tickLine:false},),jsx(RechartsYAxis,{axisLine:false,stroke:"var(--gray-9)",tickLine:false,width:52},),jsx(RechartsTooltip,{contentStyle:({ ["backgroundColor"] : "#FFFFFF", ["border"] : "1px solid #E5E8F1", ["borderRadius"] : "10px", ["fontSize"] : "12px", ["boxShadow"] : "0 8px 20px rgba(15,23,42,.08)" }),cursor:({ ["strokeWidth"] : 1, ["fill"] : "var(--gray-3)" }),itemStyle:({ ["color"] : "var(--gray-12)" }),labelStyle:({ ["color"] : "var(--gray-11)" })},),jsx(RechartsLegend,{iconType:"circle",wrapperStyle:({ ["wrapper_style"] : ({ ["fontSize"] : "11px" }) })},),jsx(RechartsArea,{activeDot:({ ["stroke"] : "var(--accent-2)", ["fill"] : "var(--accent-10)" }),dataKey:"value",fill:"#4F46E5",isAnimationActive:false,name:reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state.y_column_rx_state_,stroke:"#4F46E5",strokeWidth:2,type:"monotone",wrapperStyle:({ ["fillOpacity"] : 0.16 })},)))
    )
});
Responsivecontainer_responsivecontainer_7affce89a88ddfc4ad2f90798ff58e0b_32c100df.displayName = "ResponsiveContainer";
return Responsivecontainer_responsivecontainer_7affce89a88ddfc4ad2f90798ff58e0b_32c100df;
})();

export const Responsivecontainer_responsivecontainer_77442224d37e4c9c1d0337db11aeeff6_32c100df = /*#__PURE__*/ (() => {
const Responsivecontainer_responsivecontainer_77442224d37e4c9c1d0337db11aeeff6_32c100df = memo(({children, ...rest}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state")
    return(
        jsx(RechartsResponsiveContainer,{...mergeSlotProps(rest, ({ height:300, minHeight:10, minWidth:10, width:"100%" }))},jsx(RechartsBarChart,{data:reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state.chart_data_rx_state_,height:"100%",margin:({ ["top"] : 10, ["right"] : 16, ["left"] : 4, ["bottom"] : 6 }),width:"100%"},jsx(RechartsCartesianGrid,{stroke:"#EEF1F7",strokeDasharray:"3 3",vertical:false},),jsx(RechartsXAxis,{axisLine:false,dataKey:"name",height:28,stroke:"var(--gray-9)",tickLine:false},),jsx(RechartsYAxis,{axisLine:false,stroke:"var(--gray-9)",tickLine:false,width:52},),jsx(RechartsTooltip,{contentStyle:({ ["backgroundColor"] : "#FFFFFF", ["border"] : "1px solid #E5E8F1", ["borderRadius"] : "10px", ["fontSize"] : "12px", ["boxShadow"] : "0 8px 20px rgba(15,23,42,.08)" }),cursor:({ ["strokeWidth"] : 1, ["fill"] : "var(--gray-3)" }),itemStyle:({ ["color"] : "var(--gray-12)" }),labelStyle:({ ["color"] : "var(--gray-11)" })},),jsx(RechartsLegend,{iconType:"circle",wrapperStyle:({ ["wrapper_style"] : ({ ["fontSize"] : "11px" }) })},),jsx(RechartsBar,{dataKey:"value",fill:"#4F46E5",isAnimationActive:false,name:reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state.y_column_rx_state_,radius:[5, 5, 0, 0]},)))
    )
});
Responsivecontainer_responsivecontainer_77442224d37e4c9c1d0337db11aeeff6_32c100df.displayName = "ResponsiveContainer";
return Responsivecontainer_responsivecontainer_77442224d37e4c9c1d0337db11aeeff6_32c100df;
})();

export const Responsivecontainer_responsivecontainer_16d2239eb10010be858f767704493234_32c100df = /*#__PURE__*/ (() => {
const Responsivecontainer_responsivecontainer_16d2239eb10010be858f767704493234_32c100df = memo(({children, ...rest}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state")
    return(
        jsx(RechartsResponsiveContainer,{...mergeSlotProps(rest, ({ height:300, minHeight:10, minWidth:10, width:"100%" }))},jsx(RechartsLineChart,{data:reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state.chart_data_rx_state_,height:"100%",margin:({ ["top"] : 10, ["right"] : 16, ["left"] : 4, ["bottom"] : 6 }),width:"100%"},jsx(RechartsCartesianGrid,{stroke:"#EEF1F7",strokeDasharray:"3 3",vertical:false},),jsx(RechartsXAxis,{axisLine:false,dataKey:"name",height:28,stroke:"var(--gray-9)",tickLine:false},),jsx(RechartsYAxis,{axisLine:false,stroke:"var(--gray-9)",tickLine:false,width:52},),jsx(RechartsTooltip,{contentStyle:({ ["backgroundColor"] : "#FFFFFF", ["border"] : "1px solid #E5E8F1", ["borderRadius"] : "10px", ["fontSize"] : "12px", ["boxShadow"] : "0 8px 20px rgba(15,23,42,.08)" }),cursor:({ ["strokeWidth"] : 1, ["fill"] : "var(--gray-3)" }),itemStyle:({ ["color"] : "var(--gray-12)" }),labelStyle:({ ["color"] : "var(--gray-11)" })},),jsx(RechartsLegend,{iconType:"circle",wrapperStyle:({ ["wrapper_style"] : ({ ["fontSize"] : "11px" }) })},),jsx(RechartsLine,{activeDot:({ ["stroke"] : "var(--accent-2)", ["fill"] : "var(--accent-10)" }),dataKey:"value",dot:false,isAnimationActive:false,name:reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state.y_column_rx_state_,stroke:"#4F46E5",strokeWidth:3,type:"monotone"},),jsx(Fragment,{},(false?(jsx(Fragment,{},jsx(RechartsLine,{activeDot:({ ["stroke"] : "var(--accent-2)", ["fill"] : "var(--accent-10)" }),dataKey:"extra",dot:false,isAnimationActive:false,name:"",stroke:"#0EA5E9",strokeDasharray:"5 4",strokeWidth:2,type:"monotone"},))):(jsx(Fragment,{},))))))
    )
});
Responsivecontainer_responsivecontainer_16d2239eb10010be858f767704493234_32c100df.displayName = "ResponsiveContainer";
return Responsivecontainer_responsivecontainer_16d2239eb10010be858f767704493234_32c100df;
})();

export const Cond_comp_8198c09d1f3ce786c5054f3107fea0de_32c100df = /*#__PURE__*/ (() => {
const Cond_comp_8198c09d1f3ce786c5054f3107fea0de_32c100df = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state")
    return(
        ((reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state.chart_type_rx_state_?.valueOf?.() === "histogram"?.valueOf?.())?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_8198c09d1f3ce786c5054f3107fea0de_32c100df.displayName = "Cond";
return Cond_comp_8198c09d1f3ce786c5054f3107fea0de_32c100df;
})();

export const Cond_comp_cf2e6fea54a82b2f9ec194e48582061f_32c100df = /*#__PURE__*/ (() => {
const Cond_comp_cf2e6fea54a82b2f9ec194e48582061f_32c100df = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state")
    return(
        ((reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state.chart_type_rx_state_?.valueOf?.() === "bar"?.valueOf?.())?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_cf2e6fea54a82b2f9ec194e48582061f_32c100df.displayName = "Cond";
return Cond_comp_cf2e6fea54a82b2f9ec194e48582061f_32c100df;
})();

export const Cond_comp_d03593a2b685d7a9c59c91d0dba9ef43_32c100df = /*#__PURE__*/ (() => {
const Cond_comp_d03593a2b685d7a9c59c91d0dba9ef43_32c100df = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state")
    return(
        ((reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state.chart_type_rx_state_?.valueOf?.() === "area"?.valueOf?.())?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_d03593a2b685d7a9c59c91d0dba9ef43_32c100df.displayName = "Cond";
return Cond_comp_d03593a2b685d7a9c59c91d0dba9ef43_32c100df;
})();

export const Responsivecontainer_responsivecontainer_fe9d1deddc849081bf9b74297a8c99ea_32c100df = /*#__PURE__*/ (() => {
const Responsivecontainer_responsivecontainer_fe9d1deddc849081bf9b74297a8c99ea_32c100df = memo(({children, ...rest}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state")
    return(
        jsx(RechartsResponsiveContainer,{...mergeSlotProps(rest, ({ height:190, minHeight:10, minWidth:10, width:"100%" }))},jsx(RechartsAreaChart,{data:reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state.live_data_rx_state_,height:"100%",margin:({ ["top"] : 10, ["right"] : 16, ["left"] : 4, ["bottom"] : 6 }),width:"100%"},jsx(RechartsCartesianGrid,{stroke:"#EEF1F7",strokeDasharray:"3 3",vertical:false},),jsx(RechartsXAxis,{axisLine:false,dataKey:"name",height:22,stroke:"var(--gray-9)",tickLine:false},),jsx(RechartsYAxis,{axisLine:false,domain:["auto", "auto"],stroke:"var(--gray-9)",tickLine:false,width:44},),jsx(RechartsTooltip,{contentStyle:({ ["fontSize"] : "11px", ["borderRadius"] : "8px" }),cursor:({ ["strokeWidth"] : 1, ["fill"] : "var(--gray-3)" }),itemStyle:({ ["color"] : "var(--gray-12)" }),labelStyle:({ ["color"] : "var(--gray-11)" })},),jsx(RechartsArea,{activeDot:({ ["stroke"] : "var(--accent-2)", ["fill"] : "var(--accent-10)" }),dataKey:"value",fill:"#0EA5E9",isAnimationActive:false,name:"Live",stroke:"#0EA5E9",strokeWidth:2.4,type:"monotone",wrapperStyle:({ ["fillOpacity"] : 0.18 })},)))
    )
});
Responsivecontainer_responsivecontainer_fe9d1deddc849081bf9b74297a8c99ea_32c100df.displayName = "ResponsiveContainer";
return Responsivecontainer_responsivecontainer_fe9d1deddc849081bf9b74297a8c99ea_32c100df;
})();

export const Foreach_comp_5b15bfbff735519cefeafbd3d762bee7_32c100df = /*#__PURE__*/ (() => {
const Foreach_comp_5b15bfbff735519cefeafbd3d762bee7_32c100df = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state")
    return(
        Array.prototype.map.call(reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state.corr_labels_rx_state_ ?? [],((label_rx_state_,index_8cb9cdb6681ffce5caeab6337548eeb6)=>(jsx(RadixThemesBox,{css:({ ["width"] : "64px", ["minWidth"] : "64px", ["height"] : "24px", ["display"] : "flex", ["alignItems"] : "center", ["justifyContent"] : "center", ["overflow"] : "hidden" }),key:index_8cb9cdb6681ffce5caeab6337548eeb6},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "9px", ["color"] : "#64748B", ["whiteSpace"] : "nowrap" })},label_rx_state_)))))
    )
});
Foreach_comp_5b15bfbff735519cefeafbd3d762bee7_32c100df.displayName = "Foreach";
return Foreach_comp_5b15bfbff735519cefeafbd3d762bee7_32c100df;
})();

export const Foreach_comp_0c0f066a6f5c54c04393c018700b86d8_32c100df = /*#__PURE__*/ (() => {
const Foreach_comp_0c0f066a6f5c54c04393c018700b86d8_32c100df = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state")
    return(
        Array.prototype.map.call(reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state.corr_rows_rx_state_ ?? [],((row_rx_state_,index_7568fc3f142ccc1a353c66d311ba8675)=>(jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["gap"] : "2px", ["alignItems"] : "center" }),direction:"row",key:index_7568fc3f142ccc1a353c66d311ba8675,gap:"3"},jsx(RadixThemesBox,{css:({ ["width"] : "88px", ["minWidth"] : "88px", ["height"] : "28px", ["display"] : "flex", ["alignItems"] : "center" })},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "9px", ["color"] : "#64748B", ["fontWeight"] : "600" })},row_rx_state_?.["label"])),Array.prototype.map.call(row_rx_state_?.["cells"] ?? [],((item_rx_state_,index_40a485d5c9c05a6f4ee69f1ab708ee28)=>(jsx(RadixThemesBox,{css:({ ["background"] : item_rx_state_?.["color"], ["border"] : "1px solid #FFFFFF", ["borderRadius"] : "5px", ["width"] : "64px", ["minWidth"] : "64px", ["height"] : "28px", ["display"] : "flex", ["alignItems"] : "center", ["justifyContent"] : "center", ["cursor"] : "help" }),key:index_40a485d5c9c05a6f4ee69f1ab708ee28,title:item_rx_state_?.["tip"]},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "10px", ["fontWeight"] : "600", ["color"] : "#1E293B" })},item_rx_state_?.["v"])))))))))
    )
});
Foreach_comp_0c0f066a6f5c54c04393c018700b86d8_32c100df.displayName = "Foreach";
return Foreach_comp_0c0f066a6f5c54c04393c018700b86d8_32c100df;
})();

export const Foreach_comp_2ab3579f57fad5ee9b27cf22b46de67a_32c100df = /*#__PURE__*/ (() => {
const Foreach_comp_2ab3579f57fad5ee9b27cf22b46de67a_32c100df = memo(({children}) => {
    const reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state = useStateContext("reflex___state____state.reflexsqlite___state___base____auth_state.reflexsqlite___state___dashboard_state____dashboard_state")
    return(
        Array.prototype.map.call(reflex___state____state__reflexsqlite___state___base____auth_state__reflexsqlite___state___dashboard_state____dashboard_state.activity_rx_state_ ?? [],((item_rx_state_,index_b730c9f028f9a6d3e95f59a1eb47b018)=>(jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["gap"] : "10px", ["alignItems"] : "start", ["paddingTop"] : "6px", ["paddingBottom"] : "6px", ["borderBottom"] : "1px solid #F1F3F9", ["width"] : "100%" }),direction:"row",key:index_b730c9f028f9a6d3e95f59a1eb47b018,gap:"3"},jsx(RadixThemesBox,{css:({ ["width"] : "7px", ["height"] : "7px", ["minWidth"] : "7px", ["borderRadius"] : "999px", ["background"] : "#4F46E5", ["marginTop"] : "5px" })},),jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["gap"] : "1px", ["alignItems"] : "start" }),direction:"column",gap:"3"},jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "11px", ["fontWeight"] : "600", ["color"] : "#111827" })},item_rx_state_?.["detail"]),jsx(RadixThemesText,{as:"p",css:({ ["fontSize"] : "10px", ["color"] : "#64748B" })},(item_rx_state_?.["action"]+" \u00b7 "+item_rx_state_?.["time"])))))))
    )
});
Foreach_comp_2ab3579f57fad5ee9b27cf22b46de67a_32c100df.displayName = "Foreach";
return Foreach_comp_2ab3579f57fad5ee9b27cf22b46de67a_32c100df;
})();
