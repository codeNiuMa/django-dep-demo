import math

from django.utils.safestring import mark_safe


class Fenye(object):
    def __init__(self, request, queryset, query_dict, page_param='page'):
        self.page_items_num = 10
        self.page_param = page_param
        self.total_page = math.ceil(queryset.count() / self.page_items_num)
        self.plus = 5
        self.page = request.GET.get(page_param, default='1')
        self.query_dict = query_dict
        if self.page.isdecimal():
            self.page = int(self.page)
        else:
            self.page = 1

        if self.total_page <= (2 * self.plus + 1):
            self.start, self.end = 1, self.total_page
        else:
            if self.page < 0 or self.page > self.total_page:
                self.page = 1
            if self.page <= self.plus:
                self.start, self.end = 1, 2 * self.plus + 1
            else:
                if self.page + self.plus > self.total_page:
                    self.start, self.end = self.total_page - 2 * self.plus, self.total_page
                else:
                    self.start, self.end = self.page - self.plus, self.page + self.plus

        self.start_id = (self.page - 1) * self.page_items_num
        self.end_id = self.start_id + self.page_items_num

        self.queryset = queryset[self.start_id:self.end_id]

    def html(self):

        page_html = []
        page_html.append("<nav aria-label=\"Page navigation\" style=\"display: flex;justify-content: center;\">"
                         "<ul class=\"pagination pagination-lg\">")
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [1])
            page_html.append(f'<li><a href="?{self.query_dict.urlencode()}">首页</a></li>')
            self.query_dict.setlist(self.page_param, [self.page - 1])
            page_html.append(f'<li><a href="?{self.query_dict.urlencode()}">上一页</a></li>')

        for i in range(self.start, self.end + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                temp = f'<li class="active"><a href="?{self.query_dict.urlencode()}">{i}</a></li>'
            else:
                temp = f'<li><a href="?{self.query_dict.urlencode()}">{i}</a></li>'
            page_html.append(temp)

        if self.page < self.total_page:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            page_html.append(f'<li><a href="?{self.query_dict.urlencode()}">下一页</a></li>')
            self.query_dict.setlist(self.page_param, [self.total_page])
            page_html.append(f'<li><a href="?{self.query_dict.urlencode()}">尾页</a></li>')
        page_html.append("</ul></nav>")

        search_html = f"""
         <form style="display: flex;justify-content: center;">
            <div class="input-group" style="float: right; width: 300px;">
                <input type="text" class="form-control" placeholder="跳转页码1~{self.total_page}" name="page">
                <span class="input-group-btn">
                <button class="btn btn-default" type="submit">Go!</button>
            </span>
            </div><!-- /input-group -->
         </form>
         """
        page_html.append(search_html)
        page_string = mark_safe("".join(page_html))
        return page_string
